import json

import boto3
import requests


def _get_parameter(key):
    ssm_client = boto3.client("ssm")

    response = ssm_client.get_parameter(
        Name=key,
        WithDecryption=True,
    )

    return response["Parameter"]["Value"]


if __name__ == "__main__":
    application_id = _get_parameter(key="/AI_DISCORD_CHATBOT/APPLICATION_ID")
    bot_token = _get_parameter(key="/AI_DISCORD_CHATBOT/BOT_TOKEN")

    response = requests.post(
        url=f"https://discord.com/api/v10/applications/{application_id}/commands",
        headers={
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "name": "hello",
                "description": "チャットボットに挨拶をしよう!!",
            }
        ),
    )

    print(response.status_code)
