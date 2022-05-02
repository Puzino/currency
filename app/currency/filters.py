from currency.models import Rate

from django.forms import DateInput

import django_filters


class RateFilter(django_filters.FilterSet):
    created_gte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created', lookup_expr='date__gte',
    )
    created_lte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created', lookup_expr='date__lte',
    )

    class Meta:
        model = Rate
        fields = {
            'buy': ('gte', 'lte'),
            'sale': ('gte', 'lte'),
            'type': ('exact',),
        }
