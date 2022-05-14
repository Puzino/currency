from currency.models import ContactUsCreate, Source

import django_filters


class SourceFilter(django_filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'id': ('gte', 'lte'),
        }


class ContactFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUsCreate
        fields = {
            'id': ('gte', 'lte'),
            'created': ('gte', 'lte'),
        }
