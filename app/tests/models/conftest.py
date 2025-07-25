import boto3
import pytest
from moto import mock_dynamodb


@pytest.fixture(scope="function")
def mock_dynamodb_client():
    with mock_dynamodb():
        dynamodb = boto3.client("dynamodb", region_name="ap-northeast-1")
        dynamodb.create_table(
            TableName="users",
            KeySchema=[{"AttributeName": "user_name", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "user_name", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        dynamodb.create_table(
            TableName="channels",
            KeySchema=[{"AttributeName": "channel_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "channel_id", "AttributeType": "S"}
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        dynamodb.create_table(
            TableName="threads",
            KeySchema=[
                {"AttributeName": "thread_id", "KeyType": "HASH"},
                {"AttributeName": "created_at", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "thread_id", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "S"},
                {"AttributeName": "channel_id", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "threadsGSI",
                    "KeySchema": [
                        {"AttributeName": "channel_id", "KeyType": "HASH"},
                        {"AttributeName": "created_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                },
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        yield dynamodb
