from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .forms import SourceForm
from .models import ContactUs, Rate, Source


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


class SourceEdit(UpdateView):
    model = Source
    template_name = 'source_edit.html'
    form_class = SourceForm
    success_url = reverse_lazy('currency:source_list')


class SourceDelete(DeleteView):
    queryset = Source.objects.all()
    template_name = 'source_delete.html'
    success_url = reverse_lazy('currency:source_list')


class SourceDetail(DetailView):
    model = Source
    template_name = 'source_detail.html'
