import json
import boto3

from config import (
    AWS_REGION,
    BEDROCK_MODEL_ID
)

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION
)

def ask_claude(
    prompt: str
):

    try:

        body = {

            "messages": [
                {
                    "role": "user",

                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],

            "inferenceConfig": {

                "maxTokens": 1024,

                "temperature": 0
            }
        }

        response = (
            bedrock_runtime.invoke_model(

                modelId=BEDROCK_MODEL_ID,

                body=json.dumps(body)
            )
        )

        response_body = json.loads(
            response["body"].read()
        )

        return response_body[
            "output"
        ]["message"]["content"][0]["text"]

    except Exception as e:

        return (
            f"[LLM ERROR] {str(e)}"
        )
