from api.v1.filters import SourceFilter, ContactFilter
from api.v1.paginations import SourcePagination, ContactPagination
from api.v1.serializers import ContactSerializer, SourceSerializer

from currency.models import ContactUsCreate, Source

from django_filters import rest_framework as filters

from rest_framework import generics, viewsets
from rest_framework import filters as rest_framework_filters

from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all().order_by('id')
    serializer_class = SourceSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
    pagination_class = SourcePagination
    filterset_class = SourceFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = ('id',)
    search_fields = ['name', 'code_name', 'source_url']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactUsCreate.objects.all().order_by('id')
    serializer_class = ContactSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
    pagination_class = ContactPagination
    filterset_class = ContactFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = ('id', 'created')
    search_fields = ['name', 'reply_to', 'subject', 'body']
