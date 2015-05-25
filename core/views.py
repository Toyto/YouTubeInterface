from django.shortcuts import render
from .forms import UrlForm
from django.http import HttpResponseRedirect, HttpResponse



def index(request):
    context = {}
    template = 'core/index.html'
    return render(request, template, context)


def publish(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            return HttpResponse
    else:
        form = UrlForm()

    context = {'form': form}
    template = 'core/publish.html'
    return render(request, template, context)
# Create your views here.
