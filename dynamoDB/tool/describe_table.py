import boto3

# Load the AWS SDK for Python
dynamodb = boto3.client(
    "dynamodb", region_name="REGION", endpoint_url="http://localhost:8000"
)

# Retrieve the selected table descriptions
try:
    response = dynamodb.describe_table(TableName=input("Enter table name: "))
    print("Success", response["Table"]["KeySchema"])
except Exception as e:
    print("Error", e)
