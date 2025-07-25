import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from src.models.user import User
from src.models.channel import Channel
from src.models.thread import Thread
import bcrypt


def test_save(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(user_name, hashed_password, dynamodb=mock_dynamodb_client)

    # テストしたい関数を呼び出す
    user.save()

    # テスト結果が期待する値と一致するか確認する
    response = mock_dynamodb_client.get_item(
        TableName=User.table, Key={"user_name": {"S": user_name}}
    )
    assert response["Item"]["user_name"]["S"] == user_name
    assert user.check_password(password)


def test_get_user(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(user_name, hashed_password, dynamodb=mock_dynamodb_client)
    user.save()

    # テストしたい関数を呼び出す
    retrieved_user = User.get_user(user_name, mock_dynamodb_client)

    # テスト結果が期待する値と一致するか確認する
    assert retrieved_user.user_name == user_name
    assert retrieved_user.check_password(password)


def test_get_all(mock_dynamodb_client):
    # テストデータを設定
    user1_name = "test_user1"
    user1_password = "test_password1"
    user1_hashed_password = bcrypt.hashpw(
        user1_password.encode(), bcrypt.gensalt()
    ).decode()

    user1 = User(user1_name, user1_hashed_password, dynamodb=mock_dynamodb_client)
    user1.save()

    user2_name = "test_user2"
    user2_password = "test_password2"
    user2_hashed_password = bcrypt.hashpw(
        user2_password.encode(), bcrypt.gensalt()
    ).decode()

    user2 = User(user2_name, user2_hashed_password, dynamodb=mock_dynamodb_client)
    user2.save()

    # テストしたい関数を呼び出す
    users = User.get_all(dynamodb=mock_dynamodb_client)

    # テスト結果が期待する値と一致するか確認する
    assert len(users) == 2
    assert users[0].user_name == user1.user_name
    assert users[0].check_password(user1_password)
    assert users[1].user_name == user2.user_name
    assert users[1].check_password(user2_password)


def test_get_favorite_channels(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    favorite_channels = ["channel1", "channel2"]

    user = User(
        user_name,
        password,
        favorite_channels=favorite_channels,
        dynamodb=mock_dynamodb_client,
    )
    user.save()

    channel1 = Channel(
        "channel1",
        "channel1",
        "channel1",
        "false",
        ["user1", "user2"],
        dynamodb=mock_dynamodb_client,
    )
    channel1.save()

    channel2 = Channel(
        "channel2",
        "channel2",
        "channel2",
        "false",
        ["user1", "user2"],
        dynamodb=mock_dynamodb_client,
    )
    channel2.save()

    # テストしたい関数を呼び出す
    retrieved_favorite_channels = user.get_favorite_channels(
        dynamodb=mock_dynamodb_client
    )
    # テスト結果が期待する値と一致するか確認する
    assert len(retrieved_favorite_channels) == 2
    assert retrieved_favorite_channels[0].channel_id == favorite_channels[0]
    assert retrieved_favorite_channels[1].channel_id == favorite_channels[1]


def test_add_favorite_channel(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    favorite_channels = ["channel1", "channel2"]

    user = User(
        user_name,
        password,
        favorite_channels=favorite_channels,
        dynamodb=mock_dynamodb_client,
    )
    user.save()

    # テストしたい関数を呼び出す
    user.add_favorite_channel("channel3")
    user.get_favorite_channels(dynamodb=mock_dynamodb_client)

    # テスト結果が期待する値と一致するか確認する
    assert len(user.favorite_channels) == 3
    assert user.favorite_channels[2] == "channel3"

    response = mock_dynamodb_client.get_item(
        TableName=User.table, Key={"user_name": {"S": user_name}}
    )
    assert response["Item"]["favorite_channels"]["SS"] == [
        "channel1",
        "channel2",
        "channel3",
    ]


def test_delete_favorite_channel(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    favorite_channels = ["channel1", "channel2"]

    user = User(
        user_name,
        password,
        favorite_channels=favorite_channels,
        dynamodb=mock_dynamodb_client,
    )
    user.save()

    user.delete_favorite_channel("channel2")
    user.get_favorite_channels(dynamodb=mock_dynamodb_client)

    # テスト結果が期待する値と一致するか確認する
    assert len(user.favorite_channels) == 1
    assert user.favorite_channels[0] == "channel1"

    response = mock_dynamodb_client.get_item(
        TableName=User.table, Key={"user_name": {"S": user_name}}
    )
    assert response["Item"]["favorite_channels"]["SS"] == ["channel1"]


def test_get_favorite_threads(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    favorite_threads = ["thread1", "thread2"]

    user = User(
        user_name,
        password,
        favorite_threads=favorite_threads,
        dynamodb=mock_dynamodb_client,
    )
    user.save()

    thread1 = Thread(
        "thread1",
        "2023-01-01 00:00:00",
        "channel1",
        "test_user",
        "hello test",
        ["user1", "user2"],
        dynamodb=mock_dynamodb_client,
    )
    thread1.save()

    thread2 = Thread(
        "thread2",
        "2023-01-02 00:00:00",
        "channel1",
        "test_user",
        "hello test",
        ["user1", "user2"],
        dynamodb=mock_dynamodb_client,
    )
    thread2.save()

    # テストしたい関数を呼び出す
    retrieved_favorite_threads = user.get_favorite_threads(
        dynamodb=mock_dynamodb_client
    )

    # テスト結果が期待する値と一致するか確認する
    assert len(retrieved_favorite_threads) == 2
    assert retrieved_favorite_threads[0].thread_id == "thread1"
    assert retrieved_favorite_threads[1].thread_id == "thread2"


def test_add_favorite_thread(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    favorite_threads = ["thread1", "thread2"]

    user = User(
        user_name,
        password,
        favorite_threads=favorite_threads,
        dynamodb=mock_dynamodb_client,
    )
    user.save()

    # テストしたい関数を呼び出す
    user.add_favorite_thread("thread3")
    user.get_favorite_threads(dynamodb=mock_dynamodb_client)

    # テスト結果が期待する値と一致するか確認する
    assert len(user.favorite_threads) == 3
    assert user.favorite_threads[2] == "thread3"

    response = mock_dynamodb_client.get_item(
        TableName=User.table, Key={"user_name": {"S": user_name}}
    )
    assert response["Item"]["favorite_threads"]["SS"] == [
        "thread1",
        "thread2",
        "thread3",
    ]


def test_delete_favorite_thread(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    favorite_threads = ["thread1", "thread2"]

    user = User(
        user_name,
        password,
        favorite_threads=favorite_threads,
        dynamodb=mock_dynamodb_client,
    )
    user.save()

    user.delete_favorite_thread("thread2")
    user.get_favorite_threads(dynamodb=mock_dynamodb_client)

    # テスト結果が期待する値と一致するか確認する
    assert len(user.favorite_threads) == 1

    response = mock_dynamodb_client.get_item(
        TableName=User.table, Key={"user_name": {"S": user_name}}
    )
    assert response["Item"]["favorite_threads"]["SS"] == ["thread1"]


def test_check_password(mock_dynamodb_client):
    # テストデータを設定
    user_name = "test_user"
    password = "test_password"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(user_name, hashed_password, dynamodb=mock_dynamodb_client)
    user.save()

    # テストしたい関数を呼び出す
    is_correct = user.check_password(password)

    # テスト結果が期待する値と一致するか確認する
    assert is_correct
