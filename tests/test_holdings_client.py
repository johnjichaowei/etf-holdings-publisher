from src.holdings_client import *
import pytest

holdings_url = 'https://www.xyz.com/bla?foo=bar'
response_data = 'Dummy Response Data'

def test_read_sends_get_request(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker)
    )
    read(holdings_url)
    requests.get.assert_called_once_with(holdings_url)

def test_read_returns_content_when_OK(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker, text=response_data)
    )
    assert read(holdings_url) == response_data

def test_read_raises_exception_when_not_OK(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker, status_code=500)
    )
    with pytest.raises(HoldingsClientError) as err:
        read(holdings_url)
    assert "Failed to retrieve holdings list, status_code 500" in str(err)

def mocked_response(mocker, status_code=200, text=None):
    response = mocker.patch('requests.Response', autospec=True)
    response.status_code = status_code
    response.text = text
    return response
