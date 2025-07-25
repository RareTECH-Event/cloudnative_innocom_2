from flask import g, request, redirect, url_for, current_app as app
from functools import wraps
from src.models.session import Session
from src.models.user import User


def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # セッション ID を cookie から取得する
        session_id = request.cookies.get("session_id")

        if not session_id:
            # セッション ID がない場合は、ログインページにリダイレクトする
            return redirect(url_for("auth.login"))

        # セッションが存在するかどうかを確認する
        session = Session.get_session(session_id)
        if not session:
            # セッションが存在しない場合は、ログインページにリダイレクトする
            return redirect(url_for("auth.login"))

        # セッションに関連するユーザーが認証されているかどうかを確認する
        user = User.get_user(session.user_name)
        if not user:
            # ユーザーが存在しない場合は、ログインページにリダイレクトする
            return redirect(url_for("auth.login"))

        # 認証されている場合は、グローバルにcurrent_userをセットする
        g.current_user = user
        return f(*args, **kwargs)

    return decorated_function
