import boto3

# Set the region
dynamodb = boto3.resource(
    "dynamodb", region_name="REGION", endpoint_url="http://localhost:8000"
)

# Call DynamoDB to retrieve the list of tables
table_list = dynamodb.meta.client.list_tables(Limit=10)
table_names = table_list["TableNames"]
print("Table names are", table_names)
