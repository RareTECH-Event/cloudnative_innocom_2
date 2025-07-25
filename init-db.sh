#!/bin/sh
# This script initializes the DynamoDB tables.

set -e

echo "Waiting for DynamoDB to be ready..."
sleep 10

echo "Deleting existing tables..."
TABLES=$(aws dynamodb list-tables --endpoint-url http://dynamodb:8000 --query 'TableNames' --output text)
for table in $TABLES; do
  if [ "$table" != "" ]; then
    echo "Deleting table: $table"
    aws dynamodb delete-table --table-name "$table" --endpoint-url http://dynamodb:8000
  fi
done

echo "Waiting for tables to be deleted..."
sleep 5

echo "Creating tables..."
for f in /dynamoDB/schema/*.json; do
  echo "Creating table from $f"
  aws dynamodb create-table --cli-input-json file://"$f" --endpoint-url http://dynamodb:8000
done

echo "Waiting for tables to be created..."
sleep 5

echo "Inserting seed data..."
for f in /dynamoDB/seed/local/*_seed.json; do
  table_name=$(basename "$f" | sed 's/_seed\\.json$//')
  echo "Inserting data into $table_name from $f"
  aws dynamodb batch-write-item --request-items file://"$f" --endpoint-url http://dynamodb:8000
done

echo "Setting TTL for sessions table..."
aws dynamodb update-time-to-live --table-name sessions --time-to-live-specification '{"Enabled":true,"AttributeName":"expired_at"}' --endpoint-url http://dynamodb:8000

echo "Database initialization complete."
