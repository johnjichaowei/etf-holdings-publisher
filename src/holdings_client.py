import requests
from src.exceptions import HoldingsClientError

def read(holdings_url):
    response = requests.get(holdings_url)
    if response.status_code != 200:
        raise HoldingsClientError(
            'Failed to retrieve holdings list, status_code {}'.format(response.status_code)
        )
    return response.text
