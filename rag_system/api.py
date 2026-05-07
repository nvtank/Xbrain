from fastapi import FastAPI

from src.orchestrator import (
    run_orchestrator
)

from src.bedrock_llm import (
    ask_claude
)

app = FastAPI()

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

@app.get("/agent-chat")
def agent_chat(
    query: str
):

    results = (
        run_orchestrator(
            query
        )
    )

    prompt = f"""
You are a senior platform AI assistant.

Use ALL tool results.

Mention:
- incidents
- costs
- metrics
- exact numerical values

RESULTS:
{results}

QUESTION:
{query}
"""

    answer = ask_claude(
        prompt
    )

    sources = []

    for item in results[
        "kb_results"
    ]:

        sources.append(
            item["source"]
        )

    return {
        "question": query,
        "answer": answer,
        "sources": sources,
        "tools_used": [

            tool["tool"]

            for tool in results[
                "tool_outputs"
            ]
        ]
    }
