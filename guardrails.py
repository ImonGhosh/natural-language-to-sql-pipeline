# guardrails.py

from typing import Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable


class GuardrailResult(BaseModel):
    decision: Literal["FORBIDDEN", "PROCEED"]
    # Human-facing message to return directly to the user
    message: str
    # Cleaned / possibly rephrased version of the user question
    cleaned_question: str


def build_guardrail_chain(llm) -> Runnable:
    """
    Guardrail for NL -> SQL (READ-ONLY):
    - FORBIDDEN: any request that is NOT pure information extraction / READ-only
      (e.g. CREATE/DROP/ALTER tables, INSERT/UPDATE/DELETE/TRUNCATE, GRANT/REVOKE, etc.)
    - RUBBISH: completely off-topic, nonsense, or not a question
    - CLARIFY: about data extraction / analysis but missing context, incomplete, or unclear
    - UNKNOWN: valid, understandable question but not answerable by this dataset/agent
    - PROCEED: clear, related to the dataset, can be handled by the SQL agent
    """

    parser = PydanticOutputParser(pydantic_object=GuardrailResult)
    format_instructions = parser.get_format_instructions()

    system_msg = (
            """
            You are a strict guardrail in front of a READ-ONLY SQL agent.

            You must classify the user's input into one of two decisions:

            - "FORBIDDEN"
            - "PROCEED"

            Rules:

            1) If the user attempts to modify the database in any way, set decision = "FORBIDDEN".
            This includes any request that involves DDL, DML, or admin operations, such as:
            - CREATE, DROP, ALTER, TRUNCATE
            - INSERT, UPDATE, DELETE, MERGE
            - GRANT, REVOKE, user/role/permission changes
            - Any other operation that changes data, schema, or access control.

            2) If the user's input is gibberish,
            set decision = "FORBIDDEN".

            3) In all other cases, even if the question is incomplete,
            set decision = "PROCEED".

            For decision = "FORBIDDEN":
            - message = "Sorry, this instruction cannot be performed either due to lack of information or security reasons."
            - cleaned_question can be an empty string or a lightly cleaned version of the original input.

            For decision = "PROCEED":
            - message should normally be an empty string.
            - cleaned_question should be a cleaned-up version of the user input (or the same text if already fine).

            Always return a JSON object that matches the GuardrailResult schema:
            - decision: "FORBIDDEN" or "PROCEED"
            - message: string
            - cleaned_question: string
            """
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_msg),
            (
                "user",
                "User question:\n{question}\n\n"
                "Return ONLY JSON, no extra text.\n"
                "{format_instructions}"
            ),
        ]
    )

    # Inject the literal formatting instructions so their internal `{}` are not parsed
    prompt = prompt.partial(format_instructions=format_instructions)

    guardrail_chain: Runnable = prompt | llm | parser
    return guardrail_chain
