import json
import os

import boto3
import requests

DISCORD_APPLICATION_ID = os.environ["DISCORD_APPLICATION_ID"]
DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]


def _generate_answer(question):
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

    response = bedrock_client.converse(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=[
            {
                "role": "user",
                "content": [{"text": question}],
            }
        ],
        inferenceConfig={
            "maxTokens": 4096,
            "temperature": 0.0,
        },
        system=[
            {
                "text": (
                    "これからあなたにはQ&Aチャットボットとして振る舞ってもらいます。\n"
                    "以下の注意書きをよく読んで回答を出力してください。\n"
                    "\n"
                    "<cautions>\n"
                    "- 明るくポジティブな回答を心がけてください。\n"
                    "- 語尾には「〜だにゃん!!」「〜だにゃ?」などの猫っぽい語尾を使用してください。\n"
                    "- 一般的な口調や敬語はなるべく避けてください。\n"
                    "</cautions>\n"
                    "\n"
                    "それでは、これからユーザからの質問を与えます。"
                )
            }
        ],
    )

    return response["output"]["message"]["content"][0]["text"]


def handler(event: dict, context: dict):
    try:
        for record in event["Records"]:
            message = record["Sns"]["Message"]
            request = json.loads(message)

            question = request["data"]["options"][0]["value"]
            answer = _generate_answer(question)

            response = requests.post(
                url=f"https://discord.com/api/v10/webhooks/{DISCORD_APPLICATION_ID}/{request['token']}",
                data=json.dumps(
                    {
                        "content": answer,
                    }
                ),
                headers={
                    "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 200:
                raise ValueError(f"Discord API call failed: {response.text}")

        return None
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

        raise e
