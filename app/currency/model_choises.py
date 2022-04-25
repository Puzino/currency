from django.db import models


class RateType(models.TextChoices):
    USD = 'USD', 'Dollar'
    EUR = 'EUR', 'Euro'


class SourceCodeName(models.IntegerChoices):
    PRIVATBANK = 1, 'PrivatBank'
    MONOBANK = 2, 'MonoBank'
