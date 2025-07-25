#!/bin/bash

read -p "Enter the name of the already defined table to create: " table_name

python3 "./dynamoDB/schema/${table_name}_schema.py"
