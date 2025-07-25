import boto3
import sys
import os

if len(sys.argv) != 3:
    print("Usage: python set_ttl.py <table_name> <ttl_attribute_name>")
    sys.exit(1)

table_name = sys.argv[1]
ttl_attribute_name = sys.argv[2]


dynamodb = boto3.client(
    "dynamodb", endpoint_url=os.getenv("DB_ENDPOINT", "http://localhost:8000")
)

try:
    response = dynamodb.update_time_to_live(
        TableName=table_name,
        TimeToLiveSpecification={"Enabled": True, "AttributeName": ttl_attribute_name},
    )
    print(
        f"Successfully set TTL for table {table_name} with attribute {ttl_attribute_name} ✨"
    )
except Exception as e:
    print(f"Error setting TTL for table {table_name}: {e}")
