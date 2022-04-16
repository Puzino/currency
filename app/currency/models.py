from django.db import models

from currency import model_choises as mch  # noqa: I100


class ContactUs(models.Model):
    email_from = models.CharField(max_length=60)
    subject = models.CharField(max_length=60)
    message = models.CharField(max_length=2000)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    type = models.CharField(max_length=5, choices=mch.TYPES_RATE)  # noqa: A003 VNE003
    created = models.DateTimeField(auto_now_add=True)
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    sale = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, default=True)


class ContactUsCreate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    reply_to = models.EmailField()
    subject = models.CharField(max_length=128)
    body = models.CharField(max_length=1024)
    raw_content = models.TextField()
