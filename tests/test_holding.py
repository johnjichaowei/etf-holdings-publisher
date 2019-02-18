from src.holding import *
from decimal import Decimal

# {"holding":"Commonwealth Bank of Australia","marketValPercent":8.25647,"marketValue":1.04168334081E9,
# "symbol":"CBA","countryCode":"AU","sectorName":"Diversified Banks","numberofshares":1.4389879E7,
# "currencySymbol":"$"}

holding_dict = {
    "name": "BHP Group Ltd.",
    "symbol": "BHP",
    "sector": "Diversified Metals & Mining",
    "market_val_percent": Decimal('6.52946'),
    "market_value": Decimal('823793522.37'),
    "number_of_shares": Decimal('24066419'),
}

holding = Holding(**holding_dict)

def test_holding_sets_name_value():
    assert holding.name == holding_dict['name']

def test_holding_has_symbol_attribute():
    assert holding.symbol == holding_dict['symbol']

def test_holding_has_sector_attribute():
    assert holding.sector == holding_dict['sector']

def test_holding_has_market_value_percent_attribute():
    assert holding.market_val_percent == holding_dict['market_val_percent']

def test_holding_has_market_value_attribute():
    assert holding.market_value == holding_dict['market_value']

def test_holding_has_number_of_shares_attribute():
    assert holding.number_of_shares == holding_dict['number_of_shares']

def test_eq_compares_attributes_values():
    assert Holding(**holding_dict) == Holding(**holding_dict)
