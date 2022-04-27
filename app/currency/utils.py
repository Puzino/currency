from decimal import Decimal


def round_decimal(value: str) -> Decimal:
    places = Decimal(10) ** -2
    return Decimal(value).quantize(places)
