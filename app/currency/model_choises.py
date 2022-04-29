from django.db import models


class RateType(models.TextChoices):
    UAH = 'UAH', 'Hryvna'
    USD = 'USD', 'Dollar'
    EUR = 'EUR', 'Euro'


class SourceCodeName(models.IntegerChoices):
    PRIVATBANK = 1, 'PrivatBank'
    MONOBANK = 2, 'MonoBank'
    VKURSE = 3, 'VKurse'
    NBU = 4, 'NBU'
    AGRIGOLE = 5, 'Credit-Agricole'
