from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404


# Create your views here.

def index(request):
    return render(request=request, template_name='homepage.html')
