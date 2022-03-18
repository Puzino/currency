from django.shortcuts import HttpResponseRedirect, get_object_or_404, render

from .forms import SourceForm
from .models import ContactUs, Rate, Source


def hello_world(request):
    return render(request, 'index.html')


def contact_us_list(request):
    rates = ContactUs.objects.all().order_by('-id')
    return render(request, 'contactus_list.html', context={'rates': rates})


def rate_list(request):
    rates = Rate.objects.all().order_by('-id')
    return render(request, 'rate_list.html', context={'rates': rates})


def source_list(request):
    source = Source.objects.all().order_by('-id')
    return render(request, 'source_list.html', context={'source': source})


def source_create(request):
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect('/source/list/')
    else:
        form = SourceForm()
    return render(request, 'source_create.html', {'form': form})


def source_detail(request, pk):
    source = get_object_or_404(Source, pk=pk)
    return render(request, 'source_detail.html', context={'source': source})


def source_edit(request, pk):
    source = get_object_or_404(Source, pk=pk)
    if request.method == "POST":
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect('/source/list/')
    else:
        form = SourceForm(instance=source)
    return render(request, 'source_edit.html', context={'form': form})


def source_delete(request, pk):
    source = get_object_or_404(Source, pk=pk)
    if request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')
    return render(request, 'source_delete.html', context={'source': source})
