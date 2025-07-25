#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ENDPOINT_URL="http://localhost:8000"
FILES=("${SCRIPT_DIR}"/*_seed.json)

# insertするテーブルを同階層のファイル名から取得
tables=()
for file in "${FILES[@]}"; do
    name=$(basename "${file}" | sed 's/_seed\.json$//')
    tables+=("${name}")
done

for table_name in "${tables[@]}"
do
    ERROR_MSG=$(aws dynamodb batch-write-item \
        --request-items file://${SCRIPT_DIR}/${table_name}_seed.json \
        --endpoint-url ${ENDPOINT_URL} \
        2>&1 > /dev/null) #　不要なログが出力されるため
    
    if [ $? -eq 0 ]; then
        echo "inserted seed data for ${table_name} table successfully🐤"
    else
        # テーブルが存在しなかった場合
        if [[ $ERROR_MSG == *"ResourceNotFoundException"* ]]; then
            echo "Error: ${table_name} table does not exist"
        else
            echo "Failed to insert seed data for ${table_name} table"
        fi
    fi
done
