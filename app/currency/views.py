from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import SourceForm
from .models import ContactUs, ContactUsCreate, Rate, Source


class ContactUsList(ListView):
    queryset = ContactUs.objects.all().order_by('-id')
    template_name = 'contactus_list.html'


class RateList(ListView):
    queryset = Rate.objects.all().order_by('-id')
    template_name = 'rate_list.html'


class SourceList(ListView):
    queryset = Source.objects.all().order_by('-id')
    template_name = 'source_list.html'


class SourceCreate(CreateView):
    model = Source
    template_name = 'source_create.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceEdit(UserPassesTestMixin, UpdateView):
    model = Source
    template_name = 'source_edit.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')

    def test_func(self):
        return self.request.user.is_superuser


class SourceDelete(UserPassesTestMixin, DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')

    def test_func(self):
        return self.request.user.is_superuser


class SourceDetail(DetailView):
    model = Source
    template_name = 'source_detail.html'


class ContactUsCreateView(CreateView):
    model = ContactUsCreate
    template_name = 'contact_mail.html'
    success_url = reverse_lazy('index')
    fields = (
        'name',
        'reply_to',
        'subject',
        'body'
    )

    def _send_email(self):
        recipient = settings.EMAIL_HOST_USER
        subject = 'User Contact'
        body = f'''
            Request From: {self.object.name}
            Email to reply: {self.object.reply_to}
            Subject: {self.object.subject}

            Body: {self.object.body}
        '''
        send_mail(
            subject,
            body,
            recipient,
            [recipient],
            fail_silently=False,
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)
        self._send_email()
        return redirect
