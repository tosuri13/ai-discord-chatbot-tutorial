import json
import os
from enum import Enum

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]
WORKER_TOPIC_ARN = os.environ["WORKER_TOPIC_ARN"]


class InteractionRequestType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2


class InteractionResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5


def _validate(headers, raw_body):
    try:
        VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY)).verify(
            smessage=f"{headers['x-signature-timestamp']}{raw_body}".encode(),
            signature=bytes.fromhex(headers["x-signature-ed25519"]),
        )
    except BadSignatureError:
        return False

    return True


def _publish(message, message_attributes):
    sns_client = boto3.client("sns")
    sns_client.publish(
        TopicArn=WORKER_TOPIC_ARN,
        Message=message,
        MessageAttributes=message_attributes,
    )

    return None


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
            _publish(
                message=json.dumps(request),
                message_attributes={
                    "command": {
                        "DataType": "String",
                        "StringValue": request["data"]["name"],
                    }
                },
            )

            return json.dumps(
                {
                    "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                }
            )
        case _:
            ValueError(f"'{request_type}' is not supported.")


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
