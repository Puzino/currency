import requests
from celery import shared_task

from currency import model_choises as mch


@shared_task()
def parse_privatbank():
    from currency.models import Rate, Source

    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK)[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['ccy'])
        if not currency_type:
            continue

        sale = rate['sale']
        buy = rate['buy']

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )
