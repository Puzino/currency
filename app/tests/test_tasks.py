from unittest.mock import MagicMock

from currency.models import Rate
from currency.tasks import parse_monobank, parse_vkurse


def test_parse_monobank(mocker):
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1653685807, "rateBuy": 29.54, "rateSell": 32.5998},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1653685807, "rateBuy": 31.57, "rateSell": 34.9699},
    ]
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )

    assert request_get_mock.call_count == 0
    rate_initial_count = Rate.objects.count()

    # first exec
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # second exec, no changes
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('https://api.monobank.ua/bank/currency',)
    assert request_get_mock.call_args[1] == {}

    # third exec, one rate
    response_json = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1653685807, "rateBuy": 999, "rateSell": 999},
    ]
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1


def test_parse_vkurse(mocker):
    response_json = {
        "Dollar": {
            "buy": "32.15",
            "sale": "34.70"
        },
        "Euro": {
            "buy": "35.50",
            "sale": "36.30"
        }
    }
    request_get_mock = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    rate_initial_count = Rate.objects.count()

    # first request
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 1

    # second, no change
    parse_vkurse()

    assert Rate.objects.count() == rate_initial_count + 2
    assert request_get_mock.call_count == 2
    assert request_get_mock.call_args[0] == ('http://vkurse.dp.ua/course.json',)
    assert request_get_mock.call_args[1] == {}

    # third, one change
    response_json = {
        "Dollar": {
            "buy": "9999",
            "sale": "35.70"
        }
    }
    request_get_mock_2 = mocker.patch(
        'requests.get',
        return_value=MagicMock(json=lambda: response_json),
    )
    assert request_get_mock_2.call_count == 0
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 3
    assert request_get_mock_2.call_count == 1
