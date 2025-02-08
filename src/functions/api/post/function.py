def handler(event, context):
    try:
        return {
            "statusCode": 200,
        }
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

        return {
            "statusCode": 500,
        }
