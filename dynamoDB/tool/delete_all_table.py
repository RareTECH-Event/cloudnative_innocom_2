import boto3
import os
import glob
import re


# Create the DynamoDB service object
ddb = boto3.client("dynamodb", endpoint_url="http://localhost:8000")

# Get the script directory and schema file names
script_dir = os.path.dirname(os.path.realpath(__file__))
schema_files = glob.glob(os.path.join(script_dir, "../schema/*_schema.json"))

# Extract table names from file names and make a table list
tables = [
    re.sub(r"_schema\.json$", "", os.path.basename(file)) for file in schema_files
]

for table_name in tables:
    params = {"TableName": table_name}

    # Call DynamoDB to delete the specified table
    try:
        ddb.delete_table(**params)
        print(f"{table_name} table deleted successfully ✨")
    except ddb.exceptions.ResourceNotFoundException:
        print(f"Error: {table_name} table not found")
    except ddb.exceptions.ResourceInUseException:
        print(f"Error: {table_name} table in use")
