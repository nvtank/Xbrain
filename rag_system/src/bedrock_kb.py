import boto3

from config import (
    AWS_REGION,
    BEDROCK_KB_ID
)

bedrock_agent_runtime = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION
)

def retrieve_from_kb(
    query: str
):

    print()
    print("=" * 60)
    print("[RETRIEVAL] USER QUERY")
    print(query)
    print("=" * 60)

    response = (
        bedrock_agent_runtime.retrieve(
            knowledgeBaseId=BEDROCK_KB_ID,
            retrievalQuery={
                "text": query
            },
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": 8
                }
            }
        )
    )

    results = []

    print()
    print("[RETRIEVAL] RETRIEVED DOCUMENTS")

    for item in response[
        "retrievalResults"
    ]:

        content = item["content"]["text"]

        source = (
            item["location"]
            ["s3Location"]
            ["uri"]
            .split("/")[-1]
        )

        score = item["score"]

        print(
            f"- {source} "
            f"(score={score:.3f})"
        )
        results.append({

          "content": content,

          "source": source,

          "score": score,

          "citation":
          f"[Source: {source}]"
        })
    
    print("=" * 60)
    print()

    return results
