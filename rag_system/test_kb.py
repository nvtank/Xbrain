from src.bedrock_kb import retrieve_from_kb

results = retrieve_from_kb(
    "Who is Team Platform lead?"
)

for r in results[:3]:

    print("=" * 50)

    print("SOURCE:")
    print(r["source"])

    print()

    print("SCORE:")
    print(r["score"])

    print()

    print("CONTENT:")
    print(r["content"][:500])

    print()
