import json
import os
import time

import requests

DISCORD_APPLICATION_ID = os.environ["DISCORD_APPLICATION_ID"]
DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]


def handler(event: dict, context: dict):
    try:
        message = event["Records"][0]["Sns"]["Message"]
        request = json.loads(message)

        time.sleep(10)

        # Discord APIを使用して、「Hello!!」という固定のメッセージを送信する
        requests.post(
            url=f"https://discord.com/api/v10/webhooks/{DISCORD_APPLICATION_ID}/{request['token']}",
            data=json.dumps({"content": "Hello!!"}),
            headers={
                "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
                "Content-Type": "application/json",
            },
        )
    except Exception as exception:
        print(f"{type(exception).__name__}: {exception}")

        return {
            "statusCode": 500,
        }
