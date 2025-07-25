import os


# 共通の設定
class Config:
    DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class LocalConfig(Config):
    DEBUG = True  # 開発中にエラーが発生した場合にエラーがブラウザに表示され、デバックがしやすくなる。


class TestConfig(Config):
    TESTING = (
        True  # Flaskのテストランナーがアプリケーションをテストモードで実行。これにより、アプリケーション内のユニットテストや機能テストを実行できる
    )
