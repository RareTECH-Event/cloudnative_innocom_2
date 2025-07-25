# Flask Chat Application on AWS

これは、FlaskとDynamoDBで構築された、Slack風のチャットアプリケーションです。
インフラストラクチャはTerraformによってコード化されており、AWS ECS Fargate上で動作します。

## 主な技術スタック

- **バックエンド**: Python (Flask)
- **データベース**: Amazon DynamoDB
- **フロントエンド**: HTML, CSS (Tailwind CSS), JavaScript
- **インフラ**: Terraform, Docker
- **CI/CD**: GitHub Actions

---

## ローカル開発環境のセットアップ

ローカルで開発を行うには、DockerとDocker Composeが必要です。

1.  **リポジトリをクローンします。**
    ```bash
    git clone https://github.com/ikemura-ren/cloudnative-innocom.git
    cd cloudnative-innocom
    ```

2.  **Dockerコンテナを起動します。**
    これにより、FlaskアプリケーションとローカルのDynamoDBが起動します。
    ```bash
    docker-compose up --build
    ```

3.  **アプリケーションにアクセスします。**
    ブラウザで `http://localhost:8080` を開きます。

---

## AWSインフラストラクチャの管理

AWS上に本番環境を構築・管理するためのスクリプトが `infra` ディレクトリに用意されています。
これらのスクリプトを実行するには、ローカル環境に[AWS CLI](https://aws.amazon.com/jp/cli/)と[Terraform](https://www.terraform.io/downloads.html)がインストールされ、AWSへの認証情報が設定済みである必要があります。

### インフラのデプロイ（作成・更新）

新しい変更をデプロイ、またはインフラを新規に作成する場合は、以下のスクリプトを実行します。

このスクリプトは、自動的に以下の処理を行います。
- アプリケーションのDockerイメージをビルド
- ECR (Elastic Container Registry) にイメージをプッシュ
- Terraformを実行してAWSリソース（VPC, ECS, ALB, DynamoDBなど）を作成・更新

```bash
./infra/deploy.sh
```

実行後、Terraformが作成するリソースの計画（Plan）が表示され、確認を求められます。`yes`と入力すると、デプロイが開始されます。
完了後、アクセスURL（ALBのDNS名）が出力されます。

### インフラの削除

デプロイしたすべてのAWSリソースを削除するには、以下のスクリプトを実行します。

**���意: この操作は元に戻せません。** 実行すると、ECSサービスやDynamoDBテーブルなど、すべての関連リソースが完全に削除されます。

```bash
./infra/destroy.sh
```

実行後、Terraformが削除するリソースのリストが表示され、最終確認を求められます。`yes`と入力すると、削除が開始されます。
