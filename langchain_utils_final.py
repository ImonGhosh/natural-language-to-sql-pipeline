# langchain_utils_final.py

import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, Any

from prompts_final import final_prompt

# NEW: import the guardrail builder
from guardrails import build_guardrail_chain

from sqlalchemy import text
from decimal import Decimal

import streamlit as st


@st.cache_resource
def get_chain():
    print("Creating chain")
    db = SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # --- Chains ---

    # Guardrail chain (READ-only classifier)
    guardrail_chain = build_guardrail_chain(llm)

    # SQL generation chain (unchanged)
    generate_query = create_sql_query_chain(llm, db, final_prompt)

    # Execute SQL
    execute_query = RunnableLambda(lambda q, db=db: execute_query_raw(q, db))

    # Format table + summary
    format_table = RunnableLambda(format_as_table)
    summary_chain = build_summary_chain(llm)

    # The original "happy path" SQL chain (no guardrail)
    sql_chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | format_table
        | RunnablePassthrough.assign(note=summary_chain)
        | RunnableLambda(attach_note)
    )

    # --- Guarded flow wrapper ---

    def guarded_flow(inputs: dict) -> dict:
        """
        1. Run guardrail on the question.
        2. If decision != PROCEED -> return only guardrail message as response.
        3. If PROCEED -> run the original SQL chain.
        """
        # Run guardrail on the user question
        guardrail_result = guardrail_chain.invoke(
            {
                "question": inputs["question"]
            }
        )
        decision = guardrail_result.decision
        message = guardrail_result.message

        # Non-PROCEED: do NOT touch the DB, just return guardrail message
        if decision != "PROCEED":
            return {
                "question": inputs.get("question"),
                "query": None,
                "table": None,
                "meta": {
                    "note": message,  # this is what we show in the UI
                    "guardrail_decision": decision,
                },
            }

        # PROCEED: run the original SQL chain
        out = sql_chain.invoke(inputs)
        meta = out.get("meta") or {}
        meta["guardrail_decision"] = decision  # for UI / history if needed
        out["meta"] = meta
        return out

    # The chain we actually expose
    chain = RunnableLambda(guarded_flow)
    return chain


def build_summary_chain(llm):
    """Return a Runnable that takes the formatted table dict and produces a note string."""

    summary_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful data analyst. Given a user question, the conversation "
                "history, and a SQL result table, write a brief 1–2 sentence natural "
                "language description of what the result shows. Be concise and factual. "
                "You also provide a single line insight if possible. Use the available history to "
                "resolve pronouns or follow-up questions so your "
                "description reflects the full context.",
            ),
            MessagesPlaceholder(variable_name="history"),
            (
                "human",
                "Most recent user question:\n{question}\n\n"
                "Columns: {columns}\n\n"
                "First rows (truncated):\n{rows}\n\n"
                "Based on the conversation and the table, write a short description "
                "of what this table shows and one brief insight:",
            ),
        ]
    )

    def _prepare_summary_input(x: Dict[str, Any]) -> Dict[str, Any]:
        table = x.get("table") or {}
        cols = table.get("columns") or []
        rows = table.get("rows") or []
        return {
            "question": x.get("question", ""),
            "columns": ", ".join(cols),
            "rows": rows[:5],                 # still truncate
            # ✅ pass through the message history from format_as_table
            "history": x.get("messages", []),
        }

    return (
        RunnableLambda(_prepare_summary_input)
        | summary_prompt
        | llm
        | StrOutputParser()
    )


def attach_note(inputs: dict) -> dict:
    """Move `inputs['note']` into `inputs['meta']['note']` and return the object."""
    meta = dict(inputs.get("meta") or {})
    note = inputs.get("note")
    if note:
        meta["note"] = note
    inputs["meta"] = meta
    return inputs


def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history


def _to_python(value):
    if isinstance(value, Decimal):
        as_float = float(value)
        if as_float.is_integer():
            return int(as_float)
        return as_float
    return value


def execute_query_raw(query: str, db: SQLDatabase) -> list[dict]:
    """Return rows as list[dict[col -> value]]."""
    with db._engine.connect() as conn:
        result = conn.execute(text(query))
        cols = list(result.keys())
        rows = result.fetchall()

    out = []
    for row in rows:
        out.append({col: _to_python(val) for col, val in zip(cols, row)})
    return out


def format_as_table(inputs: dict) -> dict:
    """
    Turn SQL result into a compact table structure.
    Expected: inputs = {"question": ..., "query": ..., "result": ...}
    """
    rows = inputs["result"]

    if not rows:
        return {
            "question": inputs["question"],
            "query": inputs["query"],
            "table": {
                "columns": [],
                "rows": [],
            },
            "meta": {
                "row_count": 0,
                "note": "No rows returned for this query.",
            },
            # ✅ keep the messages so the summary chain can use history
            "messages": inputs.get("messages", []),
        }

    first = rows[0]
    if hasattr(first, "keys"):
        columns = list(first.keys())
        data_rows = [[row[col] for col in columns] for row in rows]
    else:
        raise TypeError("execute_query should return list of dicts for robust formatting.")

    return {
        "question": inputs["question"],
        "query": inputs["query"],
        "table": {
            "columns": columns,
            "rows": data_rows,
        },
        "meta": {
            "row_count": len(rows),
        },
        # ✅ keep history
        "messages": inputs.get("messages", []),
    }


def render_for_history(response) -> str:
    """
    Convert the structured response into text for ChatMessageHistory.
    If the guardrail blocked the request (decision != PROCEED),
    we only keep the guardrail message.
    """
    if not isinstance(response, dict):
        return str(response)

    meta = response.get("meta") or {}
    guardrail_decision = meta.get("guardrail_decision")

    # If guardrail blocked it, just store its message
    if guardrail_decision and guardrail_decision != "PROCEED":
        note = meta.get("note") or ""
        return note or "Your request could not be processed."

    # Original behaviour for PROCEED
    question = response.get("question")
    query = response.get("query")
    table = response.get("table") or {}
    columns = table.get("columns") or []
    rows = table.get("rows") or []
    row_count = meta.get("row_count", len(rows) if rows else 0)

    lines = []

    if question:
        lines.append(f"Question: {question}")

    if query:
        lines.append("\nSQL:")
        lines.append(query)

    if columns and rows:
        lines.append("\nResult (showing up to 5 rows):")
        header = " | ".join(columns)
        lines.append(header)
        lines.append("-" * len(header))
        max_rows = 5
        for r in rows[:max_rows]:
            lines.append(" | ".join(str(x) for x in r))
        if row_count > max_rows:
            lines.append(f"... ({row_count - max_rows} more rows not shown)")
        else:
            lines.append(f"(Total rows: {row_count})")
    elif row_count:
        lines.append(f"\n(Result rows: {row_count})")

    return "\n".join(lines)


def invoke_chain(question, messages):
    chain = get_chain()
    history = create_history(messages)
    response = chain.invoke({"question": question, "top_k": 3, "messages": history.messages})
    history.add_user_message(question)
    rendered_response = render_for_history(response)
    history.add_ai_message(rendered_response)
    return response
