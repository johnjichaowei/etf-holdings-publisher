from src.sns_client import *
import boto3
import pytest

topic_arn = 'arn:dummy:my-dummy-topic'
message = 'test message'
publish_response = { 'MessageId': '4dc72917-2e42-5d99-883d-7dfe299e0d3a' }

def test_init_sets_the_topic_arn_attribute(mocker):
    client = SnsClient(topic_arn)
    assert client.topic_arn == topic_arn

def test_enter_sets_the_topic(mocker):
    mocked_resource, mocked_sns, mocked_topic = mock_sns_topic(mocker)
    client = SnsClient(topic_arn)
    client.__enter__()
    mocked_resource.assert_called_once_with('sns')
    mocked_sns.Topic.assert_called_once_with(topic_arn)
    assert client.topic == mocked_topic

def test_enter_returns_itself(mocker):
    mock_sns_topic(mocker)
    client = SnsClient(topic_arn)
    assert client == client.__enter__()

def test_publish_publishs_the_message(mocker):
    _, _, mocked_topic = mock_sns_topic(mocker)
    with SnsClient(topic_arn) as client:
        client.publish(message)
        mocked_topic.publish.assert_called_once_with(Message=message)

def test_publish_returns_the_publish_response(mocker):
    _, _, mocked_topic = mock_sns_topic(mocker, publish_response = publish_response)
    with SnsClient(topic_arn) as client:
        assert client.publish(message) == publish_response

def mock_sns_topic(mocker, publish_response = {}):
    mocked_resource = mocker.patch('boto3.resource', autospec=True)
    mocked_sns = mocked_resource.return_value
    mocked_topic = mocked_sns.Topic.return_value
    mocked_topic.publish.return_value = publish_response
    return (mocked_resource, mocked_sns, mocked_topic)
