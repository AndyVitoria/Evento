from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def home(request):
    temp = loader.get_template('evento_site/pages/home.html')
    return HttpResponse(temp.render({}, request))
