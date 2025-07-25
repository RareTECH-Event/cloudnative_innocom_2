import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))
from src.models.channel import Channel


def test_get_all(mock_dynamodb_client):
    # Set up test data
    channel1 = Channel(
        "channel1",
        "Channel 1",
        "Description 1",
        "public",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    channel1.save()
    channel2 = Channel(
        "channel2",
        "Channel 2",
        "Description 2",
        "private",
        ["user3", "user4"],
        mock_dynamodb_client,
    )
    channel2.save()

    # Call the function you want to test
    channels = Channel.get_all(mock_dynamodb_client)

    # Check if the test result matches the expected value
    assert len(channels) == 2
    assert channels[0].channel_id == channel1.channel_id
    assert channels[0].channel_name == channel1.channel_name
    assert channels[0].description == channel1.description
    assert channels[0].is_private == channel1.is_private
    assert set(channels[0].members) == set(channel1.members)
    assert channels[1].channel_id == channel2.channel_id
    assert channels[1].channel_name == channel2.channel_name
    assert channels[1].description == channel2.description
    assert channels[1].is_private == channel2.is_private
    assert set(channels[1].members) == set(channel2.members)


def test_get_channel(mock_dynamodb_client):
    # Set up test data
    channel = Channel(
        "test_channel_id",
        "Test Channel",
        "Test Description",
        "public",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    channel.save()

    # Call the function you want to test
    retrieved_channel = Channel.get_channel("test_channel_id", mock_dynamodb_client)

    # Check if the test result matches the expected value
    assert retrieved_channel.channel_id == channel.channel_id
    assert retrieved_channel.channel_name == channel.channel_name
    assert retrieved_channel.description == channel.description
    assert retrieved_channel.is_private == channel.is_private
    assert set(retrieved_channel.members) == set(channel.members)


def test_get_channels(mock_dynamodb_client):
    # Set up test data
    channel1 = Channel(
        "channel1",
        "Channel 1",
        "Description 1",
        "public",
        ["user1", "user2"],
        mock_dynamodb_client,
    )
    channel1.save()
    channel2 = Channel(
        "channel2",
        "Channel 2",
        "Description 2",
        "private",
        ["user3", "user4"],
        mock_dynamodb_client,
    )
    channel2.save()
    channel3 = Channel(
        "channel3",
        "Channel 3",
        "Description 3",
        "private",
        ["user1", "user4"],
        mock_dynamodb_client,
    )
    channel3.save()

    # Call the function you want to test
    user1_channels = Channel.get_channels("user1", mock_dynamodb_client)

    # Check if the test result matches the expected value
    assert len(user1_channels) == 2
    assert user1_channels[0].channel_id == channel1.channel_id
    assert user1_channels[0].channel_name == channel1.channel_name
    assert user1_channels[0].description == channel1.description
    assert user1_channels[0].is_private == channel1.is_private
    assert set(user1_channels[0].members) == set(channel1.members)
    assert user1_channels[1].channel_id == channel3.channel_id
    assert user1_channels[1].channel_name == channel3.channel_name
    assert user1_channels[1].description == channel3.description
    assert user1_channels[1].is_private == channel3.is_private
    assert set(user1_channels[1].members) == set(channel3.members)

    # Call the function you want to test
    user2_channels = Channel.get_channels("user2", mock_dynamodb_client)

    # Check if the test result matches the expected value
    assert len(user2_channels) == 1
    assert user2_channels[0].channel_id == channel1.channel_id
    assert user2_channels[0].channel_name == channel1.channel_name
    assert user2_channels[0].description == channel1.description
    assert user2_channels[0].is_private == channel1.is_private
    assert set(user2_channels[0].members) == set(channel1.members)


def test_save(mock_dynamodb_client):
    # Set test data
    channel_id = "test_channel_id"
    channel_name = "test_channel_name"
    description = "test_description"
    is_private = "private"
    members = ["user1", "user2"]

    channel = Channel(
        channel_id, channel_name, description, is_private, members, mock_dynamodb_client
    )

    # Call the function you want to test
    channel.save()

    # To check if the test result matches the expected value
    response = mock_dynamodb_client.get_item(
        TableName="channels", Key={"channel_id": {"S": channel_id}}
    )
    assert response["Item"]["channel_id"]["S"] == channel_id
    assert response["Item"]["channel_name"]["S"] == channel_name
    assert response["Item"]["description"]["S"] == description
    assert response["Item"]["is_private"]["S"] == is_private
    assert set(response["Item"]["members"]["SS"]) == set(members)


def test_delete(mock_dynamodb_client):
    # Set test data
    channel_id = "test_channel_id"
    channel_name = "test_channel_name"
    description = "test_description"
    is_private = "private"
    members = ["user1", "user2"]

    # Create a new Channel object and save it to DynamoDB
    channel = Channel(
        channel_id, channel_name, description, is_private, members, mock_dynamodb_client
    )
    channel.save()

    # Call the function you want to test
    channel.delete()

    # Retrieve the deleted Channel object from DynamoDB
    response = mock_dynamodb_client.get_item(
        TableName="channels", Key={"channel_id": {"S": channel_id}}
    )

    # To check if the test result matches the expected value
    assert "Item" not in response


def test_handle_members(mock_dynamodb_client):
    # Set test data
    channel_id = "test_channel_id"
    channel_name = "test_channel_name"
    description = "test_description"
    is_private = "private"
    members = ["user1", "user2"]

    # Create a new Channel object and save it to DynamoDB
    channel = Channel(
        channel_id, channel_name, description, is_private, members, mock_dynamodb_client
    )
    channel.save()

    # Call the function you want to test
    new_user = "user3"
    channel.handle_members(new_user)

    # Retrieve the updated Channel object from DynamoDB
    response = mock_dynamodb_client.get_item(
        TableName="channels", Key={"channel_id": {"S": channel_id}}
    )

    # To check if the test result matches the expected value
    assert new_user in channel.members
    assert new_user in response["Item"]["members"]["SS"]

    # Call the function you want to test
    existing_user = "user1"
    channel.handle_members(existing_user)

    # Retrieve the updated Channel object from DynamoDB
    response = mock_dynamodb_client.get_item(
        TableName="channels", Key={"channel_id": {"S": channel_id}}
    )

    # To check if the test result matches the expected value
    assert existing_user not in channel.members
    assert existing_user not in response["Item"]["members"]["SS"]


def test_get_members(mock_dynamodb_client):
    # Set test data
    channel_id = "test_channel_id"
    channel_name = "test_channel_name"
    description = "test_description"
    is_private = "private"
    members = ["user1", "user2"]

    # Create a new Channel object and save it to DynamoDB
    channel = Channel(
        channel_id, channel_name, description, is_private, members, mock_dynamodb_client
    )
    channel.save()

    # Call the function you want to test
    channels = channel.get_members()

    # To check if the test result matches the expected value
    assert len(channels) == 1
    assert channels[0].channel_id == channel_id
    assert channels[0].channel_name == channel_name
    assert channels[0].description == description
    assert channels[0].is_private == is_private
    assert set(channels[0].members) == set(members)
