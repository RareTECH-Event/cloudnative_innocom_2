from src.models.init_db import initDynamoDB


class Channel:
    table = "channels"

    def __init__(
        self, channel_id, channel_name, description, is_private, members, dynamodb=None
    ):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.description = description
        self.is_private = is_private
        self.members = members
        self.dynamodb = dynamodb or initDynamoDB()

    @classmethod
    def get_all(cls, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        response = dynamodb.scan(TableName=cls.table)
        if "Items" in response:
            channels = []
            for item in response["Items"]:
                channel = Channel(
                    item["channel_id"]["S"],
                    item["channel_name"]["S"],
                    item["description"]["S"],
                    item["is_private"]["S"],
                    item["members"]["SS"],
                    dynamodb,
                )
                channels.append(channel)
            return channels

    @classmethod
    def get_channel(cls, channel_id, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        response = dynamodb.get_item(
            TableName=cls.table, Key={"channel_id": {"S": channel_id}}
        )
        if "Item" in response:
            channel = Channel(
                response["Item"]["channel_id"]["S"],
                response["Item"]["channel_name"]["S"],
                response["Item"]["description"]["S"],
                response["Item"]["is_private"]["S"],
                response["Item"]["members"]["SS"],
                dynamodb,
            )
            return channel

    @classmethod
    def get_channels(self, user_name, dynamodb=None):
        # current_userに表示するchannelを選択するロジック(所属していないprivate channelは表示しない)
        all_channels = Channel.get_all(dynamodb)
        channels = []
        for channel in all_channels:
            if user_name in channel.members or channel.is_private == "false":
                channels.append(channel)
        return channels

    def save(self):
        self.dynamodb.put_item(
            TableName=self.table,
            Item={
                "channel_id": {"S": self.channel_id},
                "channel_name": {"S": self.channel_name},
                "description": {"S": self.description},
                "is_private": {"S": self.is_private},
                "members": {"SS": self.members},
            },
        )

    def delete(self):
        self.dynamodb.delete_item(
            TableName=Channel.table, Key={"channel_id": {"S": self.channel_id}}
        )

    def handle_members(self, user_name):
        if user_name in self.members:
            self.dynamodb.update_item(
                TableName=Channel.table,
                Key={
                    "channel_id": {"S": self.channel_id},
                },
                UpdateExpression="DELETE members :user_name",
                ExpressionAttributeValues={
                    ":user_name": {"SS": [user_name]},
                },
            )
            self.members.remove(user_name)
        else:
            self.dynamodb.update_item(
                TableName=Channel.table,
                Key={
                    "channel_id": {"S": self.channel_id},
                },
                UpdateExpression="ADD members :user_name",
                ExpressionAttributeValues={
                    ":user_name": {"SS": [user_name]},
                },
            )
            self.members.append(user_name)

    def get_members(self):
        # channel_idからmembers配列を取得
        response = self.dynamodb.query(
            TableName=Channel.table,
            KeyConditionExpression="channel_id = :channel_id",
            ExpressionAttributeValues={":channel_id": {"S": self.channel_id}},
        )
        if "Items" in response:
            channels = []
            for item in response["Items"]:
                channel = Channel(
                    item["channel_id"]["S"],
                    item["channel_name"]["S"],
                    item["description"]["S"],
                    item["is_private"]["S"],
                    item["members"]["SS"],
                    self.dynamodb,
                )
                channels.append(channel)
            return channels
