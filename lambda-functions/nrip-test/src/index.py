import json

def lambda_handler(event, context):
    """
    AWS Lambda function that returns a greeting message.

    Parameters:
        event (dict): The event data passed to the Lambda function.
        context (object): Provides runtime information to the handler.

    Returns:
        dict: A response with status code and a greeting message.
    """
    name = event.get("name", "User")
    message = f"Hello, {name}! This is a test lambda function by Nripendra."

    return {
        "statusCode": 200,
        "body": json.dumps({"message": message})
    }
