from datetime import datetime

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

while True:

    query = input(
        "\nQuestion: "
    )

    if query.lower() in [
        "exit",
        "quit"
    ]:
        break

    #
    # Run orchestrator
    #

    results = run_orchestrator(
        query
    )

    #
    # Memory context
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

- Mention whether a document is:
    - archived
    - deprecated
    - superseded
    - current

- If database_query contains
  important_result,
  you MUST include it directly.

You are in an ongoing conversation.

Resolve references like:
- it
- its
- they
- that service

CONVERSATION HISTORY:
{memory_context}

CURRENT RESULTS:
{results}

CURRENT QUESTION:
{query}
"""

    #
    # LLM answer
    #

    answer = ask_claude(
        prompt
    )

    #
    # Output
    #

    print()
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)
    print()
    print(answer)

    #
    # Tools used
    #

    print()
    print("=" * 60)
    print("TOOLS USED")
    print("=" * 60)

    for tool in results[
        "tool_outputs"
    ]:

        print(
            f"- {tool['tool']}"
        )

    #
    # Sources
    #

    print()
    print("=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)

    kb_results = results[
        "kb_results"
    ]

    if kb_results:

        for item in kb_results:

            print(
                f"- {item['source']}"
            )

    print()

    #
    # Save memory
    #

    add_to_memory(
        query,
        answer
    )

    #
    # Session logging
    #

    with open(
        "logs/session.log",
        "a"
    ) as f:

        f.write(
            f"\n[{datetime.now()}]\n"
        )

        f.write(
            f"QUESTION: {query}\n"
        )

        f.write(
            f"ANSWER: {answer}\n"
        )	
