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
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5


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


def _publish(message, message_attributes):
    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(Name="/AI_DISCORD_CHATBOT/TOPIC_ARN")
    topic_arn = response["Parameter"]["Value"]

    sns_client = boto3.client("sns")
    sns_client.publish(
        TopicArn=topic_arn,
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
