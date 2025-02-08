import json
import os

import requests

DISCORD_APPLICATION_ID = os.environ["DISCORD_APPLICATION_ID"]
DISCORD_BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]

if __name__ == "__main__":
    response = requests.post(
        url=f"https://discord.com/api/v10/applications/{DISCORD_APPLICATION_ID}/commands",
        headers={
            "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "name": "ask",
                "description": "チャットボットに質問してみよう!!",
                "options": [
                    {
                        "name": "question",
                        "description": "質問をここに書いてね",
                        "required": True,
                        "type": 3,
                    }
                ],
            }
        ),
    )

    print(response.status_code)
