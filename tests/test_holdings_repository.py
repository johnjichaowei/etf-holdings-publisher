from src.holdings_repository import *
from decimal import Decimal
import pytest

holdings_url = 'https://www.xyz.com/bla?foo=bar'
holding_cba = {
    "holding": "Commonwealth Bank of Australia",
    "marketValPercent": 8.25647,
    "marketValue": 1.04168334081E9,
    "symbol": "CBA",
    "countryCode": "AU",
    "sectorName": "Diversified Banks",
    "numberofshares": 1.4389879E7,
    "currencySymbol": "$"
}
holding_bhp = {
    "holding": "BHP Group Ltd.",
    "marketValPercent": 6.52946,
    "marketValue": 8.2379352237E8,
    "symbol": "BHP",
    "countryCode": "AU",
    "sectorName": "Diversified Metals & Mining",
    "numberofshares": 2.4066419E7,
    "currencySymbol":"$"
}
holding_invalid = {
    "holding": "VIRGIN AUSTRALIA INTERNATIONAL HOLDINGS PTY LTD-DUMMY",
    "marketValPercent": 0.0003,
    "marketValue": 40140.29,
    "symbol": None,
    "countryCode": None,
    "sectorName": None,
    "numberofshares": 8028057.0,
    "currencySymbol": "$"
}
holdings_data = {
    "asOfDate": "2018-12-31T00:00:00-05:00",
    "sectorWeightStock": [holding_cba, holding_invalid, holding_bhp]
}
holding_cba_model = {
    "holding_name": "Commonwealth Bank of Australia",
    "holding_symbol": "CBA",
    "holding_sector": "Diversified Banks",
    "market_val_percent": Decimal('8.25647'),
    "market_value": Decimal('1041683340.81'),
    "number_of_shares": Decimal('14389879')
}
holding_bhp_model = {
    "holding_name": "BHP Group Ltd.",
    "holding_symbol": "BHP",
    "holding_sector": "Diversified Metals & Mining",
    "market_val_percent": Decimal('6.52946'),
    "market_value": Decimal('823793522.37'),
    "number_of_shares": Decimal('24066419'),
}

def test_get_calls_holdings_client(mocker):
    mocker.patch('src.holdings_client.read', autospec=True, return_value=holdings_data)
    get(holdings_url)
    src.holdings_client.read.assert_called_once_with(holdings_url)

def test_get_raises_exception_when_sectorWeightStock_not_present_in_holdings_data(mocker):
    mocker.patch('src.holdings_client.read', autospec=True, return_value={'foo': 'bar'})
    with pytest.raises(HoldingsDataFormatError) as err:
        get(holdings_url)
    assert "Holdings data format error: missing key sectorWeightStock" in str(err)

def test_get_raises_exception_when_sectorWeightStock_is_not_a_list_in_holdings_data(mocker):
    mocker.patch('src.holdings_client.read', autospec=True, return_value={'sectorWeightStock': {}})
    with pytest.raises(HoldingsDataFormatError) as err:
        get(holdings_url)
    assert "Holdings data format error: sectorWeightStock is not one list" in str(err)

def test_get_returns_valid_holdings_as_a_list(mocker):
    mocker.patch('src.holdings_client.read', autospec=True, return_value=holdings_data)
    assert get(holdings_url) == [holding_cba_model, holding_bhp_model]
