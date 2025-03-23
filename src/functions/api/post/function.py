def handler(event, context):
    try:
        return {
            "statusCode": 200,
        }
    except Exception as exception:
        print(f"{type(exception).__name__}: {exception}")

        return {
            "statusCode": 500,
        }
