from src.bedrock_kb import retrieve_from_kb
from src.bedrock_llm import ask_claude

query = input("Question: ")

results = retrieve_from_kb(query)

context = "\n\n".join([
    r["content"]
    for r in results
])

prompt = f"""
You are an internal GeekBrain AI assistant.

Answer using ONLY the provided context.

RULES:
- If multiple documents conflict,
  prefer the most recent document.
- Check dates, versions,
  and status fields carefully.
- Explain conflicts explicitly.
- Cite relevant source documents.
- If answer is unknown,
  say you do not know.

CONTEXT:
{context}

QUESTION:
{query}
"""
answer = ask_claude(prompt)

print("\nANSWER:\n")
print(answer)
