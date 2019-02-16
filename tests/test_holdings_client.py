from src.holdings_client import *
import json
import pytest

holdings_url = 'https://www.xyz.com/bla?foo=bar'
params = {'callback': CALLBACK_PARAM_VALUE}
content = '{"foo":"bar"}'
response_data = '{}{}{}'.format(PREFIX, content, SUFFIX)

def test_read_sends_get_request(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker)
    )
    read(holdings_url)
    requests.get.assert_called_once_with(holdings_url, params)

def test_read_raises_exception_when_content_prefix_format_error(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker, text='bla{}{}'.format(content, SUFFIX))
    )
    with pytest.raises(HoldingsClientResponseFormatError) as err:
        read(holdings_url)
    assert "The response text does not start with the expected prefix" in str(err)

def test_read_raises_exception_when_content_prefix_format_error(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker, text='{}{}bla'.format(PREFIX, content))
    )
    with pytest.raises(HoldingsClientResponseFormatError) as err:
        read(holdings_url)
    assert "The response text does not end with the expected suffix" in str(err)


def test_read_returns_parsed_content_as_a_dict_when_OK(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker)
    )
    assert read(holdings_url) == json.loads(content)

def test_read_raises_exception_when_not_OK(mocker):
    mocker.patch(
        'requests.get',
        autospec=True,
        return_value=mocked_response(mocker, status_code=500)
    )
    with pytest.raises(HoldingsClientError) as err:
        read(holdings_url)
    assert "Failed to retrieve holdings list, status_code 500" in str(err)

def mocked_response(mocker, status_code=200, text=response_data):
    response = mocker.patch('requests.Response', autospec=True)
    response.status_code = status_code
    response.text = text
    return response
