#!/bin/bash
# このスクリプトは、アプリケーションのDockerイメージをビルドしてECRにプッシュし、
# Terraformを使ってAWSインフラをデプロイ（作成・更新）します。

# --- 設定項目 ---
AWS_REGION="ap-northeast-1"
ECR_REPOSITORY="flask-chat-app" # ECRリポジトリ名
# ----------------

# エラーが発生した場合はスクリプトを終了
set -e

# スクリプトが設置されているディレクトリに移動
cd "$(dirname "$0")"

# AWSアカウントIDを取得
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "AWS認証情報が設定されていません。aws configureを実行してください。"
    exit 1
fi

# ECRレジストリのURL
ECR_REGISTRY="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

# ECRへのログイン
echo "ECRにログインしています..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# イメージタグを生成 (現在のGitコミットハッシュ)
IMAGE_TAG=$(git rev-parse --short HEAD)

# Dockerイメージのビルド
echo "Dockerイメージをビルドし��います... ($ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG)"
docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG -f ../app/Dockerfile.prod ../app

# Dockerイメージのプッシュ
echo "DockerイメージをECRにプッシュしています..."
docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

# 完全なイメージURL
DOCKER_IMAGE_URL="$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"

# Terraformの実行
echo "Terraformを実行しています..."
terraform init

# ALBのDNS名を出力するため、-auto-approveを外してapplyを実行
terraform apply -var="docker_image_url=$DOCKER_IMAGE_URL"

echo "--------------------------------------------------"
echo "デプロイが完了しました！"
echo "ALBのDNS名 (アクセスURL):"
terraform output alb_dns_name
echo "--------------------------------------------------"
