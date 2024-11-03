import json
import os
from enum import Enum

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


class InteractionRequestType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2


class InteractionResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4


def _validate(headers, raw_body):
    smessage = f"{headers['x-signature-timestamp']}{raw_body}".encode()
    signature = bytes.fromhex(headers["x-signature-ed25519"])
    verify_key = VerifyKey(bytes.fromhex(os.environ["DISCORD_PUBLIC_KEY"]))

    try:
        verify_key.verify(smessage, signature)
    except BadSignatureError:
        return False

    return True


def _handle_interaction(request):
    request_type = InteractionRequestType(request["type"])

    match request_type:
        case InteractionRequestType.PING:
            return json.dumps(
                {
                    "type": InteractionResponseType.PONG,
                }
            )
        case InteractionRequestType.APPLICATION_COMMAND:
            command_name = request["data"]["name"]

            if command_name == "hello":
                return json.dumps(
                    {
                        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                        "data": {
                            "content": "Hello!!",
                        },
                    }
                )
            else:
                ValueError(f"Command: /{command_name} is not supported.")
        case _:
            ValueError(f"Interaction type: {interaction_type} is not supported.")


def handler(event, context):
    try:
        if not _validate(event["headers"], event["body"]):
            return {
                "statusCode": 401,
            }

        request = json.loads(event["body"])
        response_body = _handle_interaction(request)

        return {
            "statusCode": 200,
            "body": response_body,
        }
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

        return {
            "statusCode": 500,
        }
