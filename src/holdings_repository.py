from .exceptions import HoldingsDataFormatError
from .holding_schema import HoldingSchema
from .holding import Holding
import src.holdings_client

HOLDINGS_KEY = 'sectorWeightStock'

def get(holdings_url):
    holdings_data = src.holdings_client.read(holdings_url)
    if HOLDINGS_KEY not in holdings_data:
        raise HoldingsDataFormatError('Holdings data format error: missing key {}'.format(HOLDINGS_KEY))
    if type(holdings_data[HOLDINGS_KEY]) is not list:
        raise HoldingsDataFormatError('Holdings data format error: sectorWeightStock is not one list')

    schema = HoldingSchema()
    return [
        Holding(**schema.load(item)) for item in holdings_data[HOLDINGS_KEY] if schema.validate(item) == {}
    ]
