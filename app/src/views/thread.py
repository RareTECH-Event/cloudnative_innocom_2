import uuid
from flask import Blueprint, g, render_template, request, redirect, url_for, flash
from helpers.auth import session_required
from src.models.channel import Channel
from src.models.thread import Thread
from src.models.user import User
import datetime

threadBp = Blueprint("thread", __name__, url_prefix="/threads")


@threadBp.route("/register", methods=["GET", "POST"])
@session_required
def thread_register():
    thread_id = str(uuid.uuid4())
    # プラス9時間することで日本時間にしたい
    created_at = (datetime.datetime(2024, 1, 1, 12, 30, 0)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    if request.method == "POST":
        message = request.form["message"]
        channel_id = request.form["channel_id"]
    else: # GET
        message = request.args.get("message", "GET Request Test")
        channel_id = request.args.get("channel_id")

    if not channel_id:
        flash("チャンネルIDが指定されていません。", "error")
        return redirect(url_for("root.index_channel"))

    thread = Thread(
        thread_id=thread_id,
        created_at=created_at,
        channel_id=channel_id,
        user_name=g.current_user.user_name,
        message=message,
        likes=[],
    )

    thread.save()
    return redirect(url_for("channel.channel_detail", channel_id=channel_id))


@threadBp.route("/<thread_id>/likes", methods=["POST"])
@session_required
def thread_likes(thread_id):
    thread = Thread.get_thread(thread_id)
    thread.handle_like(g.current_user.user_name)

    if g.current_user.user_name in thread.likes:
        flash("いいねしました", "success")
    else:
        flash("いいねを取り消しました", "success")

    return redirect(url_for("channel.channel_detail", channel_id=thread.channel_id))


@threadBp.route("/<thread_id>/favorite", methods=["POST"])
@session_required
def favorite_thread(thread_id):
    thread = Thread.get_thread(thread_id)

    # もしg.current_userのfavorite_threadsにthread_idがあれば"お気に入りに追加しました"を表示
    if thread_id in g.current_user.favorite_threads:
        g.current_user.delete_favorite_thread(thread_id)
        flash("お気に入りから削除しました", "success")
    else:
        g.current_user.add_favorite_thread(thread_id)
        flash("お気に入りに追加しました", "success")

    return redirect(url_for("channel.channel_detail", channel_id=thread.channel_id))


@threadBp.route("/favorite_threads", methods=["GET"])
@session_required
def favorite_threads():
    channels = Channel.get_channels(g.current_user.user_name)
    favorite_channels = g.current_user.get_favorite_channels()
    favorite_threads = g.current_user.get_favorite_threads()

    return render_template(
        "favorite_threads.html",
        user=g.current_user,
        channels=channels,
        favorite_channels=favorite_channels,
        favorite_threads=favorite_threads,
    )


@threadBp.route("/<thread_id>/edit", methods=["POST"])
@session_required
def thread_edit(thread_id):
    message = request.form["message"]
    thread = Thread.get_thread(thread_id)
    thread.message = message
    thread.save()

    flash("スレッドを編集しました", "success")
    return redirect(url_for("channel.channel_detail", channel_id=thread.channel_id))


@threadBp.route("/<thread_id>/delete", methods=["POST"])
@session_required
def thread_delete(thread_id):
    thread = Thread.get_thread(thread_id)
    channel_id = thread.channel_id

    # お気に入りに登録しているユーザーからも削除する
    users = User.get_all()
    for user in users:
        if thread_id in user.favorite_threads:
            user.delete_favorite_thread(thread_id)
            user.save()

    thread.delete()

    flash("スレッドを削除しました", "success")
    return redirect(url_for("channel.channel_detail", channel_id=channel_id))
