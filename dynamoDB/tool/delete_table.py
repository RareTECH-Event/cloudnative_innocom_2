import boto3

# Create the DynamoDB service object
ddb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

params = {"TableName": input("Enter the name of the table to delete: ")}

# Call DynamoDB to delete the specified table
try:
    ddb.delete_table(**params)
    print("Table deleted successfully!")
except ddb.exceptions.ResourceNotFoundException:
    print("Error: Table not found")
except ddb.exceptions.ResourceInUseException:
    print("Error: Table in use")
