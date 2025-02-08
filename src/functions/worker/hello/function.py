import json
import os
import time

import requests

DISCORD_APPLICATION_ID = os.environ["DISCORD_APPLICATION_ID"]
DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]


def handler(event: dict, context: dict):
    try:
        for record in event["Records"]:
            message = record["Sns"]["Message"]
            request = json.loads(message)

            time.sleep(10)

            response = requests.post(
                url=f"https://discord.com/api/v10/webhooks/{DISCORD_APPLICATION_ID}/{request['token']}",
                data=json.dumps(
                    {
                        "content": "Hello!!",
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
