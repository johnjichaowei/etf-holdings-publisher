from src.holdings_publish_service import *
from src.holding import Holding
from src.holding_schema import HoldingSchema
import src.sns_client
from decimal import Decimal
import json

holdings_url = 'https://www.xyz.com/bla?foo=bar'
topic_arn = 'arn:dummy-sns-topic'
holding1 = Holding(**{
    "name": "Commonwealth Bank of Australia",
    "symbol": "CBA",
    "sector": "Diversified Banks",
    "market_val_percent": Decimal('8.25647'),
    "market_value": Decimal('1041683340.81'),
    "number_of_shares": Decimal('14389879')
})
holding2 = Holding(**{
    "name": "BHP Group Ltd.",
    "symbol": "BHP",
    "sector": "Diversified Metals & Mining",
    "market_val_percent": Decimal('6.52946'),
    "market_value": Decimal('823793522.37'),
    "number_of_shares": Decimal('24066419')
})
holdings = [holding1, holding2]
message1 = HoldingSchema().dumps(holding1)
message2 = HoldingSchema().dumps(holding2)

def test_init_set_holdings_url_attribute(mocker):
    service = HoldingsPublishService(holdings_url, topic_arn)
    assert service.holdings_url == holdings_url

def test_init_set_topic_arn_attribute(mocker):
    service = HoldingsPublishService(holdings_url, topic_arn)
    assert service.topic_arn == topic_arn

def test_publish_retrives_holdings_using_the_repository(mocker):
    mocked_get = mock_holdings_repo(mocker)
    service = HoldingsPublishService(holdings_url, topic_arn)
    service.publish()
    mocked_get.assert_called_once_with(holdings_url)

def test_publish_creates_one_sns_client(mocker):
    mock_holdings_repo(mocker)
    mocked_client_class, _ = mock_sns_topic(mocker)
    service = HoldingsPublishService(holdings_url, topic_arn)
    service.publish()
    mocked_client_class.assert_called_once_with(topic_arn)

def test_publish_setup_the_sns_client(mocker):
    mock_holdings_repo(mocker)
    _, mocked_client = mock_sns_topic(mocker)
    service = HoldingsPublishService(holdings_url, topic_arn)
    service.publish()
    mocked_client.__enter__.assert_called_once()

def test_publish_publishes_the_retrieved_holdings_to_sns(mocker):
    mock_holdings_repo(mocker, holdings=holdings)
    _, mocked_client = mock_sns_topic(mocker)
    service = HoldingsPublishService(holdings_url, topic_arn)
    service.publish()
    mocked_client.publish.assert_any_call(message1)
    mocked_client.publish.assert_any_call(message2)
    assert mocked_client.publish.call_count == 2

def mock_holdings_repo(mocker, holdings = []):
    return mocker.patch(
        'src.holdings_repository.get',
        autospec=True,
        return_value=holdings
    )

def mock_sns_topic(mocker):
    mocked_client_class = mocker.patch('src.sns_client.SnsClient', autospec=True)
    mocked_client = mocked_client_class.return_value
    mocked_client.__enter__.return_value = mocked_client
    return (mocked_client_class, mocked_client)
