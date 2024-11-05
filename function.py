import json
from enum import Enum

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


class InteractionRequestType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2


class InteractionResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4


def _validate(headers, raw_body):
    message = f"{headers['x-signature-timestamp']}{raw_body}".encode()
    signature = bytes.fromhex(headers["x-signature-ed25519"])

    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(
        Name="/AI_DISCORD_CHATBOT/PUBLIC_KEY",
        WithDecryption=True,
    )
    public_key = response["Parameter"]["Value"]
    verify_key = VerifyKey(bytes.fromhex(public_key))

    try:
        verify_key.verify(message, signature)
    except BadSignatureError:
        return False

    return True


def _handle_interaction(request):
    request_type = InteractionRequestType(request["type"])

    match request_type:
        case InteractionRequestType.PING:
            return json.dumps(
                {
                    "type": InteractionResponseType.PONG.value,
                }
            )
        case InteractionRequestType.APPLICATION_COMMAND:
            command_name = request["data"]["name"]

            if command_name == "hello":
                return json.dumps(
                    {
                        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
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
