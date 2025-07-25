import boto3, os


def initDynamoDB():
    dynamodb = boto3.client(
        "dynamodb",
        # appを読み込むと循環参照になるため
        endpoint_url=os.environ.get("DB_ENDPOINT"),
        region_name=os.environ.get("AWS_REGION"),
    )
    return dynamodb
