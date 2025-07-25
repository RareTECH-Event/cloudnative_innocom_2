import time
import uuid
from flask import (
    Blueprint,
    make_response,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from src.models.user import User
from src.models.session import Session
from helpers.auth import session_required
import bcrypt

authBp = Blueprint("auth", __name__, url_prefix="/auth")


@authBp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]

        user = User.get_user(user_name)

        if user and user.check_password(password):
            # session_idを生成
            session_id = str(uuid.uuid4())

            # 24時間で設定
            ttl_unixtime = time.time() + (60 * 60 * 24)

            # レコードを作成
            session = Session(
                session_id=session_id,
                user_name=user_name,
                expired_at=int(ttl_unixtime),
            )
            # sessionsにレコードを追加
            session.save()

            # cookieにsession_idをセットして返す
            response = make_response(redirect(url_for("root.index_channel")))
            response.set_cookie("session_id", session_id)
            return response

        flash("ユーザーネーム または パスワード が違います", "error")
        return render_template("login.html")


@authBp.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]

        if User.get_user(user_name):
            flash("ユーザーネームが既に使われています", "error")
            return render_template("register.html")

        # passwordをハッシュ化
        hashed_password = password

        user = User(
            user_name=user_name,
            password=hashed_password,
        )
        user.save()
        return redirect(url_for("auth.login"))


@authBp.route("/logout", methods=["GET"])
@session_required
def logout():
    # sessionsテーブルからレコードを削除
    Session.delete(request.cookies.get("session_id"))

    return redirect(url_for("auth.login"))
