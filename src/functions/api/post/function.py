import json
import os

import boto3
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]
WORKER_TOPIC_ARN = os.environ["WORKER_TOPIC_ARN"]


def handler(event, context):
    try:
        # リクエスト署名の検証処理を行う
        try:
            VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY)).verify(
                smessage=f"{event['headers']['x-signature-timestamp']}{event['body']}".encode(),
                signature=bytes.fromhex(event["headers"]["x-signature-ed25519"]),
            )
        except BadSignatureError:
            return {
                "statusCode": 401,
            }

        request = json.loads(event["body"])
        match request["type"]:
            # RequestType: PING(1)の場合
            case 1:
                # ResponseType: PONG(1)を返す
                return {
                    "statusCode": 200,
                    "body": json.dumps({"type": 1}),
                }
            # RequestType: APPLICATION_COMMAND(2)の場合
            case 2:
                # トピックにイベントを公開して、後続のLambdaに回答生成の処理をさせる
                sns_client = boto3.client("sns")
                sns_client.publish(
                    TopicArn=WORKER_TOPIC_ARN,
                    Message=json.dumps(request),
                    MessageAttributes={
                        "command": {
                            "DataType": "String",
                            "StringValue": request["data"]["name"],
                        }
                    },
                )

                # ResponseType: DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE(5)を返す
                return {
                    "statusCode": 200,
                    "body": json.dumps({"type": 5}),
                }
            case _:
                ValueError(f"'{request['type']}' is not supported.")

    except Exception as exception:
        print(f"{type(exception).__name__}: {exception}")

        return {
            "statusCode": 500,
        }
