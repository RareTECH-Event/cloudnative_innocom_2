#!/bin/bash
# このスクリプトは、Terraformが何を削除しようとしているかを確認（plan）するだけで、
# 実際の削除は行いません。

# スクリプトが設置されているディレクトリに移動
cd "$(dirname "$0")"

echo "Terraformの初期化..."
terraform init

echo "AWSインフラの削除計画を生成します..."
# docker_image_url変数はplanの生成に必要だが、destroy時には実際には使われないためダミーの値を渡す
terraform plan -destroy -var="docker_image_url=dummy"

echo "--------------------------------------------------"
echo "上記の削除計画を確認してください。"
echo "実際に削除するには、destroy.sh を実行してください。"
echo "--------------------------------------------------"
