from django.shortcuts import render


def menu(request):
    context = {}
    template = 'index.html'
    return render(request, template, context)
# Create your views here.
