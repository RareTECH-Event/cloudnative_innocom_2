import os
from flask import Flask
from src.views.root import rootBp
from src.views.auth import authBp
from src.views.user import userBp
from src.views.channel import channelBp
from src.views.thread import threadBp

app = Flask(__name__, static_folder="assets/dist", template_folder="src/templates")

app.config["SECRET_KEY"] = "secret_key"

# routerをグルーピングしつつ登録
app.register_blueprint(rootBp)
app.register_blueprint(authBp)
app.register_blueprint(userBp)
app.register_blueprint(channelBp)
app.register_blueprint(threadBp)

# 環境変数 'ENV' を読み込みデバックモード等を修正する
if os.environ.get("ENV") == "prod":
    app.config.from_object("config.ProdConfig")
elif os.environ.get("ENV") == "test":
    app.config.from_object("config.TestConfig")
else:
    # ENV == local
    app.config.from_object("config.LocalConfig")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
