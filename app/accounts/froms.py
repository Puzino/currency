from django import forms

from accounts.models import User  # noqa: I100
from accounts.tasks import send_activate_email


class SignUpForm(forms.ModelForm):

    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        user = super().save(commit=False)
        user.set_password(cleaned_data['password1'])
        user.is_active = False

        if commit:
            user.save()

        send_activate_email.delay(user.username, user.email)

        return user
