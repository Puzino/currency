from currency.models import ContactUsCreate, Source
from currency.tasks import send_email

from rest_framework import serializers


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'name', 'source_url', 'code_name')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsCreate
        fields = ('id', 'created', 'name', 'reply_to', 'subject', 'body')

    def create(self, validated_data):
        send_email.delay(**validated_data)
        return ContactUsCreate.objects.create(**validated_data)
