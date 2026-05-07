from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.orchestrator import (
    run_orchestrator
)

from src.bedrock_llm import (
    ask_claude
)

from src.memory_store import (
    init_memory_db,
    load_recent_memory,
    save_message,
)

from src.utils.logger import (
    log_event,
)

from config import (
    API_KEY,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_memory_db()


class ChatRequest(BaseModel):
    session_id: str
    query: str


def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

@app.post("/agent-chat")
def agent_chat(
    req: ChatRequest,
    x_api_key: str = Header(...),
):

    verify_api_key(x_api_key)

    session_id = req.session_id
    query = req.query

    #
    # Run orchestrator
    #

    results = run_orchestrator(
        query
    )

    #
    # Memory
    #

    memory_context = (
        load_recent_memory(session_id)
    )

    #
    # Prompt
    #

    prompt = f"""
You are a senior platform AI assistant.

CRITICAL RULES:

- Use ONLY retrieved evidence.
- ALWAYS mention exact numerical values.
- NEVER ignore SQL outputs.
- Include source citations naturally.

- If multiple documents conflict:
    - compare versions
    - compare dates
    - prefer newest/current documents
    - explicitly explain conflicts

Resolve references like:
- it
- its
- they
- that service

CONVERSATION HISTORY:
{memory_context}

RESULTS:
{results}

QUESTION:
{query}
"""

    #
    # LLM
    #

    answer = ask_claude(
        prompt
    )

    log_event({
        "session_id": session_id,
        "query": query,
        "answer": answer,
        "tools_used": [
            tool["tool"]
            for tool in results["tool_outputs"]
        ],
        "latency_ms": results.get("trace", {}).get("latency_ms", 0),
        "retrieved_docs": [
            doc["source"]
            for doc in results["kb_results"]
        ],
    })

    #
    # Save memory
    #

    save_message(
        session_id,
        "user",
        query,
    )

    save_message(
        session_id,
        "assistant",
        answer,
    )

    #
    # Sources
    #

    sources = []
    citations = []

    for item in results[
        "kb_results"
    ]:

        sources.append(
            item["source"]
        )

        snippet = (
            item.get("content", "")
            .replace("\n", " ")
            .strip()
        )

        if len(snippet) > 260:
            snippet = snippet[:260].rstrip() + "..."

        citations.append({
            "source": item["source"],
            "snippet": snippet,
        })

    #
    # Response
    #

    return {

        "question":
        query,

        "answer":
        answer,

        "sources":
        sources,

        "citations":
        citations,

        "tools_used": [

            tool["tool"]

            for tool in results[
                "tool_outputs"
            ]
        ],

        "trace":
        results.get(
            "trace",
            {}
        ),

        "reasoning":
        results.get(
            "reasoning_steps",
            []
        )
    }
