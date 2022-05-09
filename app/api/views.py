from api.serializers import ContactSerializer, SourceSerializer

from currency.models import ContactUsCreate, Source

from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_csv.renderers import CSVRenderer

from rest_framework_xml.renderers import XMLRenderer


class SourceView(generics.ListAPIView):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactUsCreate.objects.all()
    serializer_class = ContactSerializer
    renderer_classes = (JSONRenderer, XMLRenderer, CSVRenderer)
