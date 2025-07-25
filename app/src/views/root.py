from flask import (
    Blueprint,
    g,
    redirect,
    url_for,
)
from src.models.channel import Channel
from helpers.auth import session_required

rootBp = Blueprint("root", __name__, url_prefix="/")


@rootBp.route("/", methods=["GET"])
@session_required
def index_channel():
    channels = Channel.get_channels(g.current_user.user_name)
    favorite_channels = g.current_user.get_favorite_channels()

    # もしチャンネルがなければ作成画面へ
    if len(channels) == 0:
        return redirect(url_for("channel.channel_register"))
    # お気に入りチャンネルがなければ適当なチャンネルへ
    elif len(channels) > 0:
        return redirect(
            url_for("channel.channel_detail", channel_id=channels[0].channel_id)
        )
    # もしチャンネルがなければ作成画面へ
    elif len(favorite_channels) > 0:
        return redirect(
            url_for(
                "channel.channel_detail", channel_id=favorite_channels[0].channel_id
            )
        )
