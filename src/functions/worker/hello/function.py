import json
import time

import boto3
import requests


def _get_parameter(key):
    ssm_client = boto3.client("ssm")

    response = ssm_client.get_parameter(
        Name=key,
        WithDecryption=True,
    )

    return response["Parameter"]["Value"]


def handler(event: dict, context: dict):
    try:
        for record in event["Records"]:
            message = record["Sns"]["Message"]
            request = json.loads(message)

            application_id = _get_parameter(key="/AI_DISCORD_CHATBOT/APPLICATION_ID")
            bot_token = _get_parameter(key="/AI_DISCORD_CHATBOT/BOT_TOKEN")

            time.sleep(10)

            response = requests.post(
                url=f"https://discord.com/api/v10/webhooks/{application_id}/{request['token']}",
                data=json.dumps(
                    {
                        "content": "Hello!!",
                    }
                ),
                headers={
                    "Authorization": f"Bot {bot_token}",
                    "Content-Type": "application/json",
                },
            )

            if response.status_code != 200:
                raise ValueError(f"Discord API call failed: {response.text}")

        return None
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

        raise e
