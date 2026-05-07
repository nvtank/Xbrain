from fastapi import FastAPI

from src.orchestrator import (
    run_orchestrator
)

from src.bedrock_llm import (
    ask_claude
)

from src.memory import (
    add_to_memory,
    get_memory
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
        get_memory()
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

    #
    # Save memory
    #

    add_to_memory(
        query,
        answer
    )

    #
    # Sources
    #

    sources = []

    for item in results[
        "kb_results"
    ]:

        sources.append(
            item["source"]
        )

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

        "tools_used": [

            tool["tool"]

            for tool in results[
                "tool_outputs"
            ]
        ]
    }
