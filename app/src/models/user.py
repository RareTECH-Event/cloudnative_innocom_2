from src.models.init_db import initDynamoDB
from src.models.channel import Channel
from src.models.thread import Thread
import bcrypt


class User:
    table = "users"

    def __init__(
        self,
        user_name,
        password,
        profile_image_url,  # Added
        favorite_channels=None,
        favorite_threads=None,
        dynamodb=None,
    ):
        self.user_name = user_name
        self.password = password
        self.profile_image_url = profile_image_url  # Added
        self.favorite_channels = favorite_channels or []
        self.favorite_threads = favorite_threads or []
        self.dynamodb = dynamodb or initDynamoDB()

    def save(self):
        item = {
            "user_name": {"S": self.user_name},
            "password": {"S": self.password},
            "profile_image_url": {"S": self.profile_image_url},  # Added
        }
        if self.favorite_channels:
            item["favorite_channels"] = {"SS": self.favorite_channels}
        if self.favorite_threads:
            item["favorite_threads"] = {"SS": self.favorite_threads}

        self.dynamodb.put_item(TableName=self.table, Item=item)

    @classmethod
    def get_user(cls, user_name, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        response = dynamodb.get_item(
            TableName=cls.table, Key={"user_name": {"S": user_name}}
        )
        if "Item" in response:
            user = User(
                response["Item"]["user_name"]["S"],
                response["Item"]["password"]["S"],
                response["Item"]["profile_image_url"]["S"],  # Changed
                response["Item"].get("favorite_channels", {}).get("SS")
                if "favorite_channels" in response["Item"]
                else [],
                response["Item"].get("favorite_threads", {}).get("SS")
                if "favorite_threads" in response["Item"]
                else [],
                dynamodb,
            )
            return user

    @classmethod
    def get_all(cls, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        response = dynamodb.scan(TableName="users")
        users = []
        for item in response["Items"]:
            user = User(
                item["user_name"]["S"],
                item["password"]["S"],
                item["profile_image_url"]["S"],  # Changed: Direct access
                item.get("favorite_channels", {}).get("SS")
                if "favorite_channels" in item
                else [],
                item.get("favorite_threads", {}).get("SS")
                if "favorite_threads" in item
                else [],
                dynamodb,
            )
            users.append(user)

        return users

    # Userのfavorite_channels配列を取得する
    def get_favorite_channels(self, dynamodb=None):
        channels = []
        for channel_id in self.favorite_channels:
            channel = Channel.get_channel(channel_id, dynamodb or self.dynamodb)
            channels.append(channel)

        return channels

    def get_favorite_threads(self, dynamodb=None):
        threads = []
        for thread_id in self.favorite_threads:
            thread = Thread.get_thread(thread_id, dynamodb or self.dynamodb)
            threads.append(thread)

        return threads

    # Userのfavorite_channelsにチャンネルを追加する
    def add_favorite_channel(self, channel_id):
        self.dynamodb.update_item(
            TableName=User.table,
            Key={
                "user_name": {"S": self.user_name},
            },
            UpdateExpression="ADD favorite_channels :channel_id",
            ExpressionAttributeValues={
                ":channel_id": {"SS": [channel_id]},
            },
        )
        self.favorite_channels.append(channel_id)

    # Userのfavorite_channelsからチャンネルを削除する
    def delete_favorite_channel(self, channel_id):
        self.dynamodb.update_item(
            TableName=User.table,
            Key={
                "user_name": {"S": self.user_name},
            },
            UpdateExpression="DELETE favorite_channels :channel_id",
            ExpressionAttributeValues={
                ":channel_id": {"SS": [channel_id]},
            },
        )
        self.favorite_channels.remove(channel_id)

    # Userのfavorite_threadsにスレッドを追加する
    def add_favorite_thread(self, thread_id):
        self.dynamodb.update_item(
            TableName=User.table,
            Key={
                "user_name": {"S": self.user_name},
            },
            UpdateExpression="ADD favorite_threads :thread_id",
            ExpressionAttributeValues={
                ":thread_id": {"SS": [thread_id]},
            },
        )
        self.favorite_threads.append(thread_id)

    # Userのfavorite_threadsからスレッドを削除する
    def delete_favorite_thread(self, thread_id):
        self.dynamodb.update_item(
            TableName=User.table,
            Key={
                "user_name": {"S": self.user_name},
            },
            UpdateExpression="DELETE favorite_threads :thread_id",
            ExpressionAttributeValues={
                ":thread_id": {"SS": [thread_id]},
            },
        )
        self.favorite_threads.remove(thread_id)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
