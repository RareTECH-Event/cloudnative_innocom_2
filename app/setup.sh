#!/bin/bash

# This shell script used in the Dockerfile.prod file to handle environment settings by mounting secret information in the production environment.

apt-get update
apt-get install -y jq

# set aws credential as env.
AWS_CREDENTIALS=$(cat /mnt/secrets-store/cloudnative-experience-app_aws_credentials)
export AWS_ACCESS_KEY_ID=$(echo $AWS_CREDENTIALS | jq -r '.AWS_ACCESS_KEY_ID')
export AWS_SECRET_ACCESS_KEY=$(echo $AWS_CREDENTIALS | jq -r '.AWS_SECRET_ACCESS_KEY')

# Run the application.
python app.py
