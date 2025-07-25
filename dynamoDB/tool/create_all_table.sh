#!/bin/bash

export AWS_ACCESS_KEY_ID='DAMMY'
export AWS_SECRET_ACCESS_KEY='DAMMY'
export AWS_DEFAULT_REGION='DAMMY'

# Get the script directory and schema file name.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
files=("${script_dir}/../schema/"*_schema.json)

# Extract table names from file names and make table list.
tables=()
for file in "${files[@]}"; do
    name=$(basename "${file}" | sed 's/_schema\.json$//')
    tables+=("${name}")
done

# Execute schema definitions for each table.
for table_name in "${tables[@]}"; do
    python3 "./dynamoDB/tool/create_table.py" "${table_name}"
    if [ "${table_name}" == "sessions" ]; then
        python3 "./dynamoDB/tool/set_ttl.py" "sessions" "expired_at"
    fi
done
