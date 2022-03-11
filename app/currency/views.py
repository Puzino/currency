from django.http import HttpResponse
from django.shortcuts import render

from currency.models import ContactUs


def hello_world(request):
    return render(request, 'index.html')


def contact_us_list(request):
    rates = ContactUs.objects.all()
    return render(request, 'contactus_list.html', {'rates': rates})
