import requests, json
from src.exceptions import HoldingsClientError, HoldingsClientResponseFormatError

CALLBACK_PARAM_VALUE = 'holdings_publisher'
PREFIX = '{}(['.format(CALLBACK_PARAM_VALUE)
SUFFIX = '])'

def read(holdings_url):
    response = requests.get(holdings_url, params={'callback': CALLBACK_PARAM_VALUE})
    if response.status_code != 200:
        raise HoldingsClientError(
            'Failed to retrieve holdings list, status_code {}'.format(response.status_code)
        )
    if response.text.startswith(PREFIX) == False:
        raise HoldingsClientResponseFormatError('The response text does not start with the expected prefix')
    if response.text.endswith(SUFFIX) == False:
        raise HoldingsClientResponseFormatError('The response text does not end with the expected suffix')
    return json.loads(response.text[len(PREFIX):-len(SUFFIX)])
