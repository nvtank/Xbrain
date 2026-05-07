import json
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

from src.utils.history import get_history

API_URL = "http://localhost:8001/agent-chat"
API_KEY = "super-secret-key"

st.set_page_config(
    page_title="GeekBrain AI Dashboard",
    layout="wide",
)

st.title("GeekBrain AI Operations Dashboard")

session_id = st.text_input(
    "Session ID",
    value="demo_user",
)

query = st.text_input(
    "Ask a question",
    value=(
        "Why did PaymentGW reliability drop and how much "
        "infrastructure cost did it incur in Q1 2026?"
    ),
)

if st.button("Ask AI"):

    with st.spinner("Thinking..."):

        response = requests.post(
            API_URL,
            headers={
                "x-api-key": API_KEY,
            },
            json={
                "session_id": session_id,
                "query": query,
            },
        )

        data = response.json()

    st.subheader("Final Answer")
    st.write(data.get("answer", ""))

    st.subheader("Reasoning Steps")
    for step in data.get("reasoning", []):
        st.write(f"- {step}")

    st.subheader("Reasoning Timeline")
    for i, step in enumerate(data.get("reasoning", [])):
        st.write(f"{i + 1}. {step}")

    st.subheader("Tools Used")
    st.json(data.get("tools_used", []))

    st.subheader("Trace Data")
    st.json(data.get("trace", {}))

    st.subheader("Tool Execution Tree")
    trace = data.get("trace", {})
    st.write("Question")
    st.write(f"└── {trace.get('query', '')}")

    st.write("Retrieval")
    for doc in trace.get("retrieved_docs", []):
        st.write(
            f"    ├── {doc.get('source', '')} "
            f"(score={doc.get('score', '')})"
        )

    st.write("Tools")
    for tool in trace.get("tools_called", []):
        st.write(f"    ├── {tool.get('tool', '')}")

    st.write("SQL")
    for sql in trace.get("sql_queries", []):
        st.code(sql)

    st.subheader("Retrieved Documents")
    retrieved_docs = trace.get("retrieved_docs", [])

    if retrieved_docs:
        docs_df = pd.DataFrame(retrieved_docs)
        st.dataframe(docs_df)

        fig = px.bar(
            docs_df,
            x="source",
            y="score",
            title="Retrieval Scores",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.subheader("SQL Queries")
    st.json(trace.get("sql_queries", []))

    st.subheader("Latency")
    st.metric(
        "Latency (ms)",
        trace.get("latency_ms", 0),
    )

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Latency",
        f"{trace.get('latency_ms', 0)} ms",
    )
    col2.metric(
        "Retrieved Docs",
        len(trace.get("retrieved_docs", [])),
    )
    col3.metric(
        "Tools Used",
        len(data.get("tools_used", [])),
    )

    st.subheader("Conversation History")
    history = get_history(session_id)
    for role, content in history:
        st.write(f"**{role.upper()}**: {content}")

    st.subheader("Latency Distribution")
    events = []
    try:
        with open("logs/trace.jsonl") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                events.append(json.loads(line))
    except FileNotFoundError:
        events = []

    if events:
        logs_df = pd.DataFrame(events)
        if "latency_ms" in logs_df.columns:
            fig = px.histogram(
                logs_df,
                x="latency_ms",
                title="Latency Distribution",
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
            )
