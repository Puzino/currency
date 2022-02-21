from currency.models import ContactUs

from django.http import HttpResponse


# Create your views here.
def hello_world(request):
    return HttpResponse('Hello, world!')


def contact_us_list(request):
    rates = [[contact.id, contact.email_from, contact.subject, contact.message] for contact in ContactUs.objects.all()]
    return HttpResponse(str(rates))
