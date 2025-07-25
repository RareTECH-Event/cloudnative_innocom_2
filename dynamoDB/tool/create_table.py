import sys
import boto3
import json
import os
from botocore.exceptions import ClientError

# Get argument
if len(sys.argv) != 2:
    print("Usage: python create_dynamodb_table.py <table_name>")
    sys.exit(1)

table_name = sys.argv[1]

# Set the region
dynamodb = boto3.resource(
    "dynamodb",
    region_name="REGION",
    endpoint_url=os.getenv("DB_ENDPOINT", "http://localhost:8000"),
)


try:
    # Load the schema from the file
    with open(f"./dynamoDB/schema/{table_name}_schema.json", "r") as f:
        schema = json.load(f)

    # Create the DynamoDB table
    table = dynamodb.create_table(**schema)

    # Wait until the table exists
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)

    print(f"create {table_name} table successfully 🦄")

except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceInUseException":
        print("Error: the Table is already exists")
    else:
        print("Unexpected error: %s" % e)
