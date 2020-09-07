from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context, loader

from . import *

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def dashboard(request):
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render())

def devices(request):
    template = loader.get_template("devices.html")
    return HttpResponse(template.render())

def plans(request):
    template = loader.get_template("plans.html")
    return HttpResponse(template.render())

def statistics(request):
    template = loader.get_template("statistics.html")
    return HttpResponse(template.render())

def weather(request):
    template = loader.get_template("weather.html")
    return HttpResponse(template.render())

def settings(request):
    template = loader.get_template("settings.html")
    return HttpResponse(template.render())

def help(request):
    template = loader.get_template("help.html")
    return HttpResponse(template.render())
