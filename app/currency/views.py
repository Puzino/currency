from django.shortcuts import render

from .models import ContactUs, Rate


def hello_world(request):
    return render(request, 'index.html')


def contact_us_list(request):
    rates = ContactUs.objects.all()
    return render(request, 'contactus_list.html', {'rates': rates})


def rate_list(request):
    rates = Rate.objects.all()
    return render(request, 'rate_list.html', {'rates': rates})
