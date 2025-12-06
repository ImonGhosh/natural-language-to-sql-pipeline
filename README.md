# Natural Language to SQL Pipeline

A Streamlit app that converts natural-language questions into safe, grounded MySQL queries, executes them, and returns compact result tables with short insights. The pipeline is designed for small research-oriented datasets and can be adapted to any MySQL database by updating table metadata and few-shot examples.

## Key Features
- **Guarded execution:** A LangChain guardrail blocks non-read operations and gibberish before any database access, keeping the pipeline read-only and safe.
- **Context-rich SQL generation:** Dynamic few-shot retrieval and table-aware prompting steer SQL generation toward relevant schemas without scanning the entire database.
- **Conversation memory:** Chat history is threaded through SQL generation and summarization so follow-up questions can be incomplete while still grounded in prior turns.
- **Result rendering with insight:** Query outputs are formatted into compact tables and summarized into concise 1–2 sentence notes for quick interpretation.
- **Streamlit chat UI:** Users chat with the assistant, inspect the generated SQL, and view results directly in the app.

## Workflow Overview
1. **User asks a question** in the Streamlit chat UI.
2. **Conversation memory is refreshed** from previous turns so pronouns or shorthand follow-ups retain context across the chain.
3. **Guardrail classification** decides whether the request is safe (read-only and meaningful). Blocked requests return an immediate explanation without running SQL.
4. **Table selection** uses table descriptions to choose relevant tables for the prompt, limiting query scope.
5. **SQL synthesis** leverages LangChain with dynamic few-shot examples and the table context to build a MySQL query.
6. **Execution & formatting** run the query, convert rows to a compact table, and compute row counts.
7. **Summarization** produces a brief description and optional insight about the returned data, using chat history for context.

## Setup
1. Install Python dependencies (requires Python 3.10+):
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your MySQL and OpenAI credentials:
   ```bash
   db_user="<username>"
   db_password="<password>"
   db_host="<host>"
   db_name="<schema>"
   OPENAI_API_KEY="<openai-key>"
   LANGCHAIN_API_KEY="<optional-langchain-key>"
   LANGCHAIN_PROJECT="<optional-project-name>"
   ```
3. (Optional) Enable LangSmith tracing by exporting `LANGCHAIN_TRACING_V2=true`.

## Running the App
From the repository root:
```bash
streamlit run main.py
```
The app starts a chat interface where you can submit natural-language questions, view generated SQL (via the “Inspect SQL query” expander), and see compact results with notes.

## Customizing for Your Database
- **Table descriptions:** Update `database_table_descriptions.csv` with short descriptions for every table. This drives automatic table selection.
- **Few-shot examples:** Update `examples_final.py` with task-specific Q&A pairs related to your database. Ideally, include the queries and metrics most relevant and expected for your database.

## Safety & Grounding
- Guardrails prevent any CREATE/INSERT/UPDATE/DELETE/ALTER/GRANT-style operations and reject gibberish or off-topic inputs before SQL runs.
- Only selected tables are exposed to the model, reducing the risk of broad, unfocused queries.

## Future Directions
- Add dashboards or analytic visualizations on top of query results.
- Introduce batching and caching to better serve medium-sized datasets.
- Extend guardrails with semantic data policies (e.g., column-level access rules).
