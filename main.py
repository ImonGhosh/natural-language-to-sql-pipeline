# main.py

import streamlit as st
import pandas as pd
from openai import OpenAI
from langchain_utils_final import invoke_chain

st.title("Natural Language to SQL Chatbot for Market Research")

client = OpenAI(api_key="sk-proj-A7w7Tc7hDDSIijauF-...")  # unchanged

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about the market, for data and insight"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = invoke_chain(prompt, st.session_state.messages)

            meta = response.get("meta", {}) or {}
            note = meta.get("note")
            guardrail_decision = meta.get("guardrail_decision")

            # --- Case 1: Guardrail blocked or redirected (NOT PROCEED) ---
            if guardrail_decision and guardrail_decision != "PROCEED":
                # Just show the guardrail message, nothing else
                if note:
                    st.markdown(note)
                else:
                    st.markdown("Sorry, this instruction cannot be performed due to security reasons.")

            # --- Case 2: Normal SQL flow (PROCEED / no guardrail info) ---
            else:
                # Optional: show SQL query
                query = response.get("query")
                if query:
                    with st.expander("Inspect SQL query"):
                        st.code(query, language="sql")

                table = response.get("table") or {}
                columns = table.get("columns") or []
                rows = table.get("rows") or []

                if columns and rows:
                    df = pd.DataFrame(rows, columns=columns)
                    st.markdown("**Result:**")
                    st.dataframe(df, use_container_width=True)
                else:
                    st.markdown("No rows were returned.")

                if note:
                    st.markdown(f"**Note:** {note}")

    # Store only the natural-language output (note/guardrail message) in history
    st.session_state.messages.append(
        {"role": "assistant", "content": (response.get("meta", {}) or {}).get("note", "")}
    )