from django import forms

from .models import Rate, Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url', 'logotype')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('type', 'source', 'buy', 'sale')
