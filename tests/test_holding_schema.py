from src.holding_schema import *
from decimal import Decimal

def test_data_key_for_holding_name():
    schema = HoldingSchema(only=['name'])
    result = {'name': 'Commonwealth Bank of Australia'}
    assert schema.loads('{"holding":"Commonwealth Bank of Australia"}') == result

def test_holding_name_is_required():
    schema = HoldingSchema(only=['name'])
    assert schema.validate({}) == {'holding': ['Missing data for required field.']}

def test_holding_name_can_not_be_empty():
    schema = HoldingSchema(only=['name'])
    assert schema.validate({'holding': ''}) == {'holding': ["Holding name can't be empty."]}

def test_holding_name_can_not_be_only_white_spaces():
    schema = HoldingSchema(only=['name'])
    assert schema.validate({'holding': '   '}) == {'holding': ["Holding name can't be only white spaces."]}

def test_data_key_for_holding_symbol():
    schema = HoldingSchema(only=['symbol'])
    result = {'symbol': 'CBA'}
    assert schema.loads('{"symbol":"CBA"}') == result

def test_holding_symbol_is_required():
    schema = HoldingSchema(only=['symbol'])
    assert schema.validate({}) == {'symbol': ['Missing data for required field.']}

def test_holding_symbol_can_not_be_empty():
    schema = HoldingSchema(only=['symbol'])
    assert schema.validate({'symbol': ''}) == {'symbol': ["Holding symbol can't be empty."]}

def test_holding_symbol_can_not_be_only_white_spaces():
    schema = HoldingSchema(only=['symbol'])
    assert schema.validate({'symbol': '   '}) == {'symbol': ["Holding symbol can't be only white spaces."]}

def test_data_key_for_holding_sector():
    schema = HoldingSchema(only=['sector'])
    result = {'sector': 'Diversified Banks'}
    assert schema.loads('{"sectorName":"Diversified Banks"}') == result

def test_data_key_for_market_val_percent():
    schema = HoldingSchema(only=['market_val_percent'])
    result = {'market_val_percent': Decimal('8.25647')}
    assert schema.loads('{"marketValPercent":8.25647}') == result

def test_market_val_percent_must_be_a_valid_number():
    schema = HoldingSchema(only=['market_val_percent'])
    assert schema.validate({'marketValPercent': 'bla'}) == {'marketValPercent': ['Not a valid number.']}

def test_data_key_for_market_value():
    schema = HoldingSchema(only=['market_value'])
    result = {'market_value': Decimal('1041683340.81')}
    assert schema.loads('{"marketValue":1.04168334081E9}') == result

def test_market_value_must_be_a_valid_number():
    schema = HoldingSchema(only=['market_value'])
    assert schema.validate({'marketValue': 'bla'}) == {'marketValue': ['Not a valid number.']}

def test_data_key_for_():
    schema = HoldingSchema(only=['number_of_shares'])
    result = {'number_of_shares': Decimal('14389879')}
    assert schema.loads('{"numberofshares":1.4389879E7}') == result

def test_market_value_must_be_a_valid_number():
    schema = HoldingSchema(only=['number_of_shares'])
    assert schema.validate({'numberofshares': 'bla'}) == {'numberofshares': ['Not a valid number.']}

def test_schema_excludes_unknown_field():
    assert HoldingSchema().unknown == EXCLUDE

def test_dumps_can_serialize_the_data():
    holding = {
        "name": "Commonwealth Bank of Australia",
        "symbol": "CBA",
        "sector": "Diversified Banks",
        "market_val_percent": Decimal('8.25647'),
        "market_value": Decimal('1041683340.81'),
        "number_of_shares": Decimal('14389879')
    }
    expected_json_str = '{"holding": "Commonwealth Bank of Australia", "symbol": "CBA", "sectorName": "Diversified Banks", "marketValPercent": "8.25647", "marketValue": "1041683340.81", "numberofshares": "14389879"}'
    assert HoldingSchema().dumps(holding) == expected_json_str
