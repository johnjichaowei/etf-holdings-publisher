import requests, json
from src.exceptions import HoldingsClientError, HoldingsDataFormatError

CALLBACK_PARAM_VALUE = 'holdings_publisher'
PREFIX = '{}(['.format(CALLBACK_PARAM_VALUE)
SUFFIX = '])'

def read(holdings_url):
    response = requests.get(holdings_url, params={'callback': CALLBACK_PARAM_VALUE})
    if response.status_code != 200:
        raise HoldingsClientError(
            'Failed to retrieve holdings list, status_code {}'.format(response.status_code)
        )
    if not response.text.startswith(PREFIX):
        raise HoldingsDataFormatError('The response text does not start with the expected prefix')
    if not response.text.endswith(SUFFIX):
        raise HoldingsDataFormatError('The response text does not end with the expected suffix')
    return json.loads(response.text[len(PREFIX):-len(SUFFIX)])
