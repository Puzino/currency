from django import forms

from .models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ('name', 'source_url')
