from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context, loader
from django.template.response import TemplateResponse

from . import *

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def dashboard(request):
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render())

def devices(request):
    
    args = {}

    # GET variables

    args['filter_name'] = request.GET.get('name', '')

    args['filter_device'] = request.GET.get('device', '')

    args['filter_status'] = request.GET.get('status', '')
    

    return TemplateResponse(request, "devices.html", args)

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
