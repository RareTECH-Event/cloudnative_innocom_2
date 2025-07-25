import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from src.models.thread import Thread


def test_save(mock_dynamodb_client):
    # Set up test data
    thread = Thread(
        "test_thread_id",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test_channel_id",
        "test_user_name",
        "test_message",
        ["user1", "user2"],
        mock_dynamodb_client,
    )

    # Call the function you want to test
    thread.save()

    # Check if the test result matches the expected value
    retrieved_thread = Thread.get_thread("test_thread_id", mock_dynamodb_client)
    assert retrieved_thread.thread_id == thread.thread_id
    assert retrieved_thread.created_at == thread.created_at
    assert retrieved_thread.channel_id == thread.channel_id
    assert retrieved_thread.user_name == thread.user_name
    assert retrieved_thread.message == thread.message
    assert set(retrieved_thread.likes) == set(thread.likes)


def test_get_all_threads(mock_dynamodb_client):
    now = datetime.now()

    # Set up test data
    thread1 = Thread(
        "thread1",
        (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"),
        "channel1",
        "user_name",
        "hello test",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    thread1.save()
    thread2 = Thread(
        "thread2",
        (now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "channel1",
        "user_name",
        "hello test",
        ["user3", "user4"],
        mock_dynamodb_client,
    )
    thread2.save()

    # Call the function you want to test
    threads = Thread.get_all_threads(
        channel_id="channel1", dynamodb=mock_dynamodb_client
    )

    print(threads[0].created_at)

    # Check if the test result matches the expected value
    assert len(threads) == 2
    assert threads[0].thread_id == thread1.thread_id
    assert threads[0].created_at == thread1.created_at
    assert threads[0].channel_id == thread1.channel_id
    assert threads[0].user_name == thread1.user_name
    assert threads[0].message == thread1.message
    assert set(threads[0].likes) == set(thread1.likes)


def test_get_thread(mock_dynamodb_client):
    # Set up test data
    thread = Thread(
        "test_thread_id",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test_channel_id",
        "test_user_name",
        "test_message",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    thread.save()

    # Call the function you want to test
    retrieved_thread = Thread.get_thread("test_thread_id", mock_dynamodb_client)

    # Check if the test result matches the expected value
    assert retrieved_thread.thread_id == thread.thread_id
    assert retrieved_thread.created_at == thread.created_at
    assert retrieved_thread.channel_id == thread.channel_id
    assert retrieved_thread.user_name == thread.user_name
    assert retrieved_thread.message == thread.message
    assert set(retrieved_thread.likes) == set(thread.likes)


def test_handle_like(mock_dynamodb_client):
    # Set up test data
    thread = Thread(
        "test_thread_id",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test_channel_id",
        "test_user_name",
        "test_message",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    thread.save()

    # Call the function you want to test
    thread.handle_like("user3")

    # Check if the test result matches the expected value
    retrieved_thread = Thread.get_thread("test_thread_id", mock_dynamodb_client)
    assert set(retrieved_thread.likes) == set(["user1", "user2", "user3"])

    # Call the function you want to test
    thread.handle_like("user1")

    # Check if the test result matches the expected value
    retrieved_thread = Thread.get_thread("test_thread_id", mock_dynamodb_client)
    assert set(retrieved_thread.likes) == set(["user2", "user3"])

    # Call the function you want to test
    thread.handle_like("user3")

    # Check if the test result matches the expected value
    retrieved_thread = Thread.get_thread("test_thread_id", mock_dynamodb_client)
    assert set(retrieved_thread.likes) == set(["user2"])


def test_delete(mock_dynamodb_client):
    # Set up test data
    thread = Thread(
        "test_thread_id",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test_channel_id",
        "test_user_name",
        "test_message",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    thread.save()

    # Call the function you want to test
    thread.delete()

    # Check if the test result matches the expected value
    retrieved_thread = Thread.get_thread("test_thread_id", mock_dynamodb_client)
    assert retrieved_thread is None
