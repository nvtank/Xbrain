from src.tools.api_tool import (
    get_incidents
)

from src.bedrock_llm import ask_claude

incidents = get_incidents()

prompt = f"""
You are an SRE assistant.

Summarize the major incidents
that affected PaymentGW.

INCIDENTS:
{incidents}
"""

answer = ask_claude(prompt)

print()
print(answer)
print()
