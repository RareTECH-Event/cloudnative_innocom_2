import uuid
from flask import Blueprint, g, render_template, request, redirect, url_for, flash
from src.models.channel import Channel
from src.models.thread import Thread
from src.models.user import User
from helpers.auth import session_required


channelBp = Blueprint("channel", __name__, url_prefix="/channels")


@channelBp.route("/<channel_id>", methods=["GET"])
@session_required
def channel_detail(channel_id):
    channel = Channel.get_channel(channel_id)
    channels = Channel.get_channels(g.current_user.user_name)
    favorite_channels = g.current_user.get_favorite_channels()
    threads = Thread.get_all_threads(channel_id)

    return render_template(
        "channel.html",
        user=g.current_user,
        channel=channel,
        channels=channels,
        favorite_channels=favorite_channels,
        threads=threads,
    )


@channelBp.route("/register", methods=["GET", "POST"])
@session_required
def channel_register():
    if request.method == "GET":
        channels = Channel.get_channels(g.current_user.user_name)
        favorite_channels = g.current_user.get_favorite_channels()

        return render_template(
            "channel_register.html",
            user=g.current_user,
            channels=channels,
            favorite_channels=favorite_channels,
        )

    if request.method == "POST":
        channel_id = str(uuid.uuid4())
        channel_name = request.form["channelname"]
        channel_detail = request.form.get("channeldetail")
        channel_is_private = request.form.get("is_private")
        channel = Channel(
            channel_id=channel_id,
            channel_name=channel_name,
            description=channel_detail,
            is_private=channel_is_private or "false",
            members=[g.current_user.user_name],
        )

        channel.save()
        flash("チャンネルを作成しました", "success")
        return redirect(url_for("channel.channel_detail", channel_pk=channel_id))


@channelBp.route("/<channel_id>/edit", methods=["GET", "POST"])
@session_required
def channel_edit(channel_id):
    if request.method == "GET":
        channel = Channel.get_channel(channel_id)
        channels = Channel.get_channels(g.current_user.user_name)
        favorite_channels = g.current_user.get_favorite_channels()

        return render_template(
            "channel_edit.html",
            user=g.current_user,
            channel=channel,
            channels=channels,
            favorite_channels=favorite_channels,
        )

    if request.method == "POST":
        channel_name = request.form["channelname"]
        channel_detail = request.form["channeldetail"]
        channel_is_private = request.form.get("is_private")

        channel = Channel.get_channel(channel_id)
        channel.description = channel_detail
        channel.is_private = channel_is_private or "false"
        channel.save()

        flash("チャンネルを編集しました", "success")
        return redirect(url_for("channel.channel_detail", channel_id=channel_id))


@channelBp.route("/<channel_id>/delete", methods=["POST"])
@session_required
def channel_delete(channel_id):
    channel = Channel.get_channel(channel_id)
    if not channel:
        flash("指定したチャンネルは存在しません。", "error")
        return redirect(url_for("root.index_channel"))

    users = User.get_all()
    for user in users:
        if channel_id in user.favorite_channels:
            user.delete_favorite_channel(channel_id)
        # チャンネルに紐づくスレッドをお気に入りから削除する
        for thread_id in user.favorite_threads:
            thread = Thread.get_thread(thread_id)
            if thread and thread.channel_id == channel_id:
                user.delete_favorite_thread(thread_id)

    threads = Thread.get_all_threads(channel_id)
    for thread in threads:
        thread.delete()

    channel.delete()

    flash("チャンネルを削除しました", "success")
    return redirect(url_for("root.index_channel"))


@channelBp.route("/<channel_id>/favorite", methods=["POST"])
@session_required
def channel_favorite(channel_id):
    # もしg.current_userのfavorite_channelsにchannel_idがあれば"お気に入りに追加しました"を表示
    if channel_id in g.current_user.favorite_channels:
        g.current_user.delete_favorite_channel(channel_id)
        flash("お気に入りから削除しました", "success")
    else:
        g.current_user.add_favorite_channel(channel_id)
        flash("お気に入りに追加しました", "success")

    return redirect(url_for("channel.channel_detail", channel_id=channel_id))


@channelBp.route("/<channel_id>/members/add", methods=["GET", "POST"])
@session_required
def add_channel_member(channel_id):
    if request.method == "GET":
        channel = Channel.get_channel(channel_id)
        channels = Channel.get_channels(g.current_user.user_name)
        favorite_channels = g.current_user.get_favorite_channels()

        # 現在メンバーではないUserを表示する
        users = User.get_all()
        another_members = []
        for user in users:
            if user.user_name not in channel.members:
                another_members.append(user)

        return render_template(
            "add_channel_members.html",
            user=g.current_user,
            channel=channel,
            channels=channels,
            favorite_channels=favorite_channels,
            another_members=another_members,
        )

    if request.method == "POST":
        user_name = request.form["user_name"]

        if User.get_user(user_name) is None:
            flash("指定したユーザーは存在しません", "error")
            return redirect(
                url_for("channel.add_channel_member", channel_id=channel_id)
            )

        channel = Channel.get_channel(channel_id)
        channel.handle_members(user_name)

        flash("メンバーを追加しました", "success")
        return redirect(url_for("channel.add_channel_member", channel_id=channel_id))


@channelBp.route("/<channel_id>/members/delete", methods=["GET", "POST"])
@session_required
def delete_channel_member(channel_id):
    if request.method == "GET":
        channel = Channel.get_channel(channel_id)
        channels = Channel.get_channels(g.current_user.user_name)
        favorite_channels = g.current_user.get_favorite_channels()

        # 現在メンバーののUserを表示する
        users = User.get_all()
        members = []
        for user in users:
            if user.user_name in channel.members:
                members.append(user)

        return render_template(
            "delete_channel_members.html",
            user=g.current_user,
            owner=channel.members[-1],
            channel=channel,
            channels=channels,
            favorite_channels=favorite_channels,
            members=members,
        )

    if request.method == "POST":
        user_name = request.form["user_name"]
        channel = Channel.get_channel(channel_id)
        channel.handle_members(user_name)

        flash("メンバーを削除しました", "success")
        return redirect(url_for("channel.delete_channel_member", channel_id=channel_id))
