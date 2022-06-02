from datetime import datetime, timedelta

from currency import model_choises as mch
from currency.models import Rate, Source
from currency.tasks import round_decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

import requests


class Command(BaseCommand):
    help = 'Parse Privatbank archive rates'  # noqa: A003, VNE003

    def handle(self, *args, **options):
        url = 'https://api.privatbank.ua/p24api/exchange_rates'

        today = datetime.now(tz=timezone.utc)
        date_start = datetime.now(tz=timezone.utc) - timedelta(days=365 * 6)
        total_days = (today - date_start).days

        available_currencies = {
            'USD': mch.RateType.USD,
            'EUR': mch.RateType.EUR,
            'UAH': mch.RateType.UAH,
        }

        try:
            source = Source.objects.get(code_name=mch.SourceCodeName.PRIVATBANK)
        except Source.DoesNotExist:
            source = Source.objects.create(code_name=mch.SourceCodeName.PRIVATBANK, name='PrivatBank', url=url)

        for day in range(total_days):
            current_day = date_start + timedelta(days=day)
            params = {
                'json': '',
                'date': current_day.strftime("%d.%m.%Y"),
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            rates = response.json()

            for rate in rates["exchangeRate"]:
                if len(rate) < 5:
                    continue
                if 'currency' not in rate or rate['currency'] not in available_currencies:
                    continue

                currency_type = available_currencies.get(rate['currency'])

                if not currency_type:
                    continue

                base_currency_type = available_currencies.get(rate['baseCurrency'])

                sale = round_decimal(rate['saleRate'])
                buy = round_decimal(rate['purchaseRate'])

                try:
                    Rate.objects.get(
                        source=source,
                        type=currency_type,
                        base_type=base_currency_type,
                        sale=sale,
                        buy=buy,
                        created__date=current_day
                    )
                except Rate.DoesNotExist:
                    Rate.objects.create(
                        type=currency_type,
                        base_type=base_currency_type,
                        sale=sale,
                        buy=buy,
                        source=source,
                        created=current_day
                    )
