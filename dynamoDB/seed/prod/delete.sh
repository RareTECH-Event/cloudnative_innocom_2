#!/bin/bash
set +x

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

delete_table() {
    local table_name=$1

    # # Delete the table if it already exists.
    aws dynamodb describe-table --table-name "${table_name}" --profile koyasu --no-cli-pager 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Deleting table $table_name..."
        aws dynamodb delete-table --table-name "${table_name}" --profile koyasu >/dev/null
        aws dynamodb wait table-not-exists --table-name "${table_name}" --profile koyasu
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
    delete_table "${table_name}"
done
