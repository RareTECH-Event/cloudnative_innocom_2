from src.models.init_db import initDynamoDB
from datetime import datetime, timedelta


class Thread:
    table = "threads"

    def __init__(
        self,
        thread_id,
        created_at,
        channel_id,
        user_name,
        message,
        likes=None,
        dynamodb=None,
    ):
        self.thread_id = thread_id
        self.created_at = created_at
        self.channel_id = channel_id
        self.user_name = user_name
        self.message = message
        self.likes = likes if likes else []
        self.dynamodb = dynamodb or initDynamoDB()

    def save(self):
        item = {
            "thread_id": {"S": self.thread_id},
            "created_at": {"S": self.created_at},
            "channel_id": {"S": self.channel_id},
            "user_name": {"S": self.user_name},
            "message": {"S": self.message},
        }

        if self.likes:
            item["likes"] = {"SS": self.likes}

        self.dynamodb.put_item(TableName=self.table, Item=item)

    @classmethod
    def get_all_threads(cls, channel_id, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        now = datetime.now() + timedelta(hours=9)
        past = now - timedelta(days=365 * 10)

        response = dynamodb.query(
            TableName=Thread.table,
            IndexName="threadsGSI",
            KeyConditionExpression="channel_id = :channel_id AND created_at BETWEEN :start_date AND :end_date",
            ExpressionAttributeValues={
                ":channel_id": {"S": channel_id},
                ":start_date": {"S": past.strftime("%Y-%m-%d %H:%M:%S")},
                ":end_date": {"S": now.strftime("%Y-%m-%d %H:%M:%S")},
            },
        )

        if "Items" in response:
            threads = []
            for item in response["Items"]:
                thread = Thread(
                    item["thread_id"]["S"],
                    item["created_at"]["S"],
                    item["channel_id"]["S"],
                    item["user_name"]["S"],
                    item["message"]["S"],
                    item.get("likes", {}).get("SS") if "likes" in item else [],
                    dynamodb,
                )
                threads.append(thread)
            return threads

    @classmethod
    def get_thread(cls, thread_id, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        response = dynamodb.query(
            TableName=cls.table,
            KeyConditionExpression="thread_id = :thread_id",
            ExpressionAttributeValues={":thread_id": {"S": thread_id}},
        )
        if "Items" in response and len(response["Items"]) > 0:
            item = response["Items"][0]
            thread = Thread(
                item["thread_id"]["S"],
                item["created_at"]["S"],
                item["channel_id"]["S"],
                item["user_name"]["S"],
                item["message"]["S"],
                item.get("likes", {}).get("SS") if "likes" in item else [],
                dynamodb,
            )
            return thread

    def handle_like(self, user_name):
        if user_name in self.likes:
            self.dynamodb.update_item(
                TableName=self.table,
                Key={
                    "thread_id": {"S": self.thread_id},
                    "created_at": {"S": self.created_at},
                },
                UpdateExpression="DELETE likes :user_name",
                ExpressionAttributeValues={":user_name": {"SS": [user_name]}},
            )
            self.likes.remove(user_name)
        else:
            self.dynamodb.update_item(
                TableName=self.table,
                Key={
                    "thread_id": {"S": self.thread_id},
                    "created_at": {"S": self.created_at},
                },
                UpdateExpression="ADD likes :user_name",
                ExpressionAttributeValues={":user_name": {"SS": [user_name]}},
            )
            self.likes.append(user_name)

    def delete(self):
        self.dynamodb.delete_item(
            TableName=self.table,
            Key={
                "thread_id": {"S": self.thread_id},
                "created_at": {"S": self.created_at},
            },
        )
