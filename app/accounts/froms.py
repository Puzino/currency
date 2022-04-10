from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from accounts.models import User  # noqa: I100


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

        self._send_activate_email(user)

        return user

    def _send_activate_email(self, user):
        subject = 'Регистрация'
        message_body = f'''
                Activatod Link:
                {settings.HTTP_SCHEME}://{settings.DOMAIN}{reverse('accounts:activate_user', args=[user.username])}
                '''
        recipient = settings.EMAIL_HOST_USER
        send_mail(
            subject,
            message_body,
            recipient,
            [user.email],
            fail_silently=False,
        )
