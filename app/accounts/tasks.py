from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@shared_task()
def debug():
    print('Hello From Celery Task')  # noqa: T001


@shared_task()
def send_activate_email(username: str, email: str):
    subject = 'Регистрация'
    message_body = f'''
    Activated Link:
    {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:activate_user', args=[username])}
    '''
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message_body,
        email_from,
        [email],
        fail_silently=False,
    )
