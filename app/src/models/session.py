from src.models.init_db import initDynamoDB
from src.models.user import User


class Session:
    table = "sessions"

    def __init__(
        self,
        session_id,
        user_name,
        expired_at,
        dynamodb=None,
    ):
        self.session_id = session_id
        self.user_name = user_name
        self.expired_at = expired_at
        self.dynamodb = dynamodb or initDynamoDB()

    def save(self):
        item = {
            "session_id": {"S": self.session_id},
            "user_name": {"S": self.user_name},
            "expired_at": {"N": str(self.expired_at)},
        }
        self.dynamodb.put_item(TableName=self.table, Item=item)

    @classmethod
    def get_session(cls, session_id, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        response = dynamodb.get_item(
            TableName=cls.table, Key={"session_id": {"S": session_id}}
        )
        if "Item" in response:
            user_name = response["Item"]["user_name"]["S"]
            user = User.get_user(user_name)
            return user

    @classmethod
    def delete(cls, session_id, dynamodb=None):
        dynamodb = dynamodb or initDynamoDB()
        dynamodb.delete_item(
            TableName=cls.table,
            Key={
                "session_id": {"S": session_id},
            },
        )
