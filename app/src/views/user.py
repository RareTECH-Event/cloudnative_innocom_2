from flask import (
    Blueprint,
    g,
    render_template,
)
from src.models.user import User
from src.models.channel import Channel
from helpers.auth import session_required

userBp = Blueprint("users", __name__, url_prefix="/users")


@userBp.route("/", methods=["GET"])
@session_required
def users():
    users = User.get_all()
    channels = Channel.get_channels(g.current_user.user_name)
    favorite_channels = g.current_user.get_favorite_channels()
    return render_template(
        "users.html",
        users=users,
        channels=channels,
        favorite_channels=favorite_channels,
    )
