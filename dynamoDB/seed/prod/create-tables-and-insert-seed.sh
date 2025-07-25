#!/bin/bash
set +x

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

create_table_and_insert_seed() {
    local table_name=$1

    # # Delete the table if it already exists.
    aws dynamodb describe-table --table-name "${table_name}" --no-cli-pager 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Deleting table $table_name..."
        aws dynamodb delete-table --table-name "${table_name}" >/dev/null
        aws dynamodb wait table-not-exists --table-name "${table_name}"
    fi

    # Create the table using a schema file.
    echo "Creating table $table_name..."
    aws dynamodb create-table \
        --cli-input-json file://${script_dir}/../../schema/${table_name}_schema.json \
        >/dev/null
    aws dynamodb wait table-exists --table-name "${table_name}"

    # Enable time-to-live for the "sessions" table
    if [ "${table_name}" == "sessions" ]; then
        aws dynamodb update-time-to-live --table-name "${table_name}" --time-to-live-specification "Enabled=true,AttributeName=expired_at" >/dev/null
    fi

    # Insert seed data into the table.
    echo "Inserting seed data..."
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
    seed_file="${script_dir}/${table_name}_seed.json"
    if [ -f "$seed_file" ]; then
        aws dynamodb batch-write-item \
            --request-items file://${seed_file} \
            >/dev/null
    else
        echo "Seed file ${seed_file} not found. Skipping seed data insertion."
    fi
}

# Get the script directory and schema file name.
files=("${script_dir}/../../schema/"*_schema.json)
tables=()

# Extract table names from file names.
for file in "${files[@]}"; do
    name=$(basename "${file}" | sed 's/_schema\.json$//')
    tables+=("${name}")
done

# Execute schema definitions for each table.
for table_name in "${tables[@]}"; do
    create_table_and_insert_seed "${table_name}"
done
