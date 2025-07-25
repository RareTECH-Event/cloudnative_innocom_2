#!/bin/bash
# このスクリプトは、Terraformで作成されたすべてのAWSリソースを自動的に削除します。
# 実行する前に、plan-destroy.sh で削除内容を必ず確認してください。

# スクリプトが設置されているディレクトリに移動
cd "$(dirname "$0")"

echo "Terraformの初期化..."
terraform init

echo "AWSインフラの削除を自動承認で開始します。"
echo "5秒後に開始します... (中断する場合は Ctrl+C)"
sleep 5

# docker_image_url変数はplanの生成に必要だが、destroy時には実際には使われないためダミーの値を渡す
terraform destroy -auto-approve -var="docker_image_url=dummy"

echo "インフラの削除が完了しました。"