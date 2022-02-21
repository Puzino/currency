from django.db import models


class ContactUs(models.Model):
    email_from = models.CharField(max_length=60)
    subject = models.CharField(max_length=60)
    message = models.CharField(max_length=2000)
