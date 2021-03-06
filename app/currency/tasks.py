from bs4 import BeautifulSoup

from celery import shared_task

from currency import model_choises as mch
from currency.models import ContactUs
from currency.utils import round_decimal

from django.conf import settings
from django.core.mail import send_mail

import requests


@shared_task()
def send_email(name, reply_to, subject, body):
    recipient = settings.EMAIL_HOST_USER
    message = f'''
        Request From: {name}
        Email to reply: {reply_to}
        Subject: {subject}

        Message: {body}
    '''
    send_mail(
        subject,
        message,
        recipient,
        [recipient],
        fail_silently=False,
    )

    ContactUs.objects.create(email_from=reply_to,
                             subject=subject,
                             message=body)


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
        'UAH': mch.RateType.UAH,
    }
    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.PRIVATBANK, name='PrivatBank')[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['ccy'])
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['base_ccy'])

        sale = round_decimal(rate["sale"])
        buy = round_decimal(rate['buy'])

        last_rate = Rate.objects \
            .filter(source=source, type=currency_type) \
            .order_by('-created').first()

        if (last_rate is None or  # does not exist in table
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task()
def parse_monobank():
    from currency.models import Rate, Source
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        840: mch.RateType.USD,
        978: mch.RateType.EUR,
        980: mch.RateType.UAH

    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.MONOBANK, name='MonoBank')[0]

    for rate in rates[:2]:
        currency_type = available_currencies.get(rate['currencyCodeA'])
        if not currency_type:
            continue

        base_currency_type = available_currencies.get(rate['currencyCodeB'])

        sale = round_decimal(rate['rateSell'])
        buy = round_decimal(rate['rateBuy'])

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=base_currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task()
def parse_vkurse():
    from currency.models import Rate, Source
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'Dollar': mch.RateType.USD,
        'Euro': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.VKURSE, name='Vkurse')[0]

    for rate in rates:
        currency_type = available_currencies.get(rate)
        if not currency_type:
            continue
        buy = round_decimal(rates.get(rate)['buy'])
        sale = round_decimal(rates.get(rate)['sale'])

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=mch.RateType.UAH,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task()
def parse_nbu():
    from currency.models import Rate, Source
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    response = requests.get(url)
    response.raise_for_status()
    rates = response.json()
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.NBU, name='NBU')[0]

    for rate in rates:
        currency_type = available_currencies.get(rate['cc'])
        if not currency_type:
            continue

        sale = 0
        buy = rate['rate']

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()

        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=mch.RateType.UAH,
                sale=sale,
                buy=buy,
                source=source,
            )


@shared_task()
def parse_credit_agricole():
    from currency.models import Rate, Source
    url = 'https://credit-agricole.ua/ru/kurs-valyut'
    response = requests.get(url).text

    rates = BeautifulSoup(response, 'html.parser')
    available_currencies = {
        'USD': mch.RateType.USD,
        'EUR': mch.RateType.EUR,
    }

    source = Source.objects.get_or_create(code_name=mch.SourceCodeName.AGRIGOLE, name='Credit-Agricole')[0]

    kurs = rates.find('div', class_="exchange-rates-table")
    currency = kurs.find_all('div', class_="currency")

    for rate in currency:
        money = rate.text.split()
        currency_type = available_currencies.get(money[0])

        if not currency_type:
            continue

        buy = money[1]
        sale = money[2]

        last_rate = Rate.objects.filter(source=source, type=currency_type).order_by('-created').first()
        if (last_rate is None or
                last_rate.sale != sale or
                last_rate.buy != buy):
            Rate.objects.create(
                type=currency_type,
                base_type=mch.RateType.UAH,
                sale=sale,
                buy=buy,
                source=source,
            )
