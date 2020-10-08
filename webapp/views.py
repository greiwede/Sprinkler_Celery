from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context, loader
from django.template.response import TemplateResponse

from .models import *

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def dashboard(request):
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render())

def devices(request):
    
    # Edit Key:
    # Pumpe = 2
    # Sensor = 1
    # Sprinkler = 0
    

    args = {}

    # GET variables
    args['filter_name'] = request.GET.get('name', '')
    args['filter_device'] = request.GET.get('device', '')
    args['filter_status'] = request.GET.get('status', '')

    check = 0


    if args['filter_device'] == 'Pumpe':
        q = Pump.objects
        args['edit_key'] = 2
        args['type_name'] = 'pump'

    if args['filter_device'] == 'Sensor':
        q = Sensor.objects
        args['edit_key'] = 1
        args['type_name'] = 'sensor'

    if args['filter_device'] == 'Sprinkler':
        q = Sprinkler.objects
        args['edit_key'] = 0
        args['type_name'] = 'sprinkler'
    
    if args['filter_device'] == '':
        q = Sprinkler.objects
        args['edit_key'] = 0
        args['filter_device'] = 'Sprinkler'
        args['type_name'] = 'sprinkler'

    if(args['filter_name']!=''):
        q = q.filter(name__contains=args['filter_name'])
        check = 1
    if(args['filter_status'] == 'OK' or args['filter_status'] == 'Warnung' or args['filter_status'] == 'Fehler'):
        q = q.filter(status__contains=args['filter_status'])
        check = 1

    if(check == 0):
        q = q.all()


    args['devices'] = q

    return TemplateResponse(request, "devices.html", args)

def device_start(request, device_type, device_id):

    args = {}

    if device_type == 0:
        print('Sprinkler mit der ID ', device_id, ' gestartet.')
        return redirect('/devices/?device=Sprinkler')
    if device_type == 1:
        print('Sensor mit der ID ', device_id, ' gestartet.')
        return redirect('/devices/?device=Sensor')
    if device_type == 2:
        print('Pumpe mit der ID ', device_id, ' gestartet.')
        return redirect('/devices/?device=Pumpe')

    

    return redirect('devices')

def device_stop(request, device_type, device_id):

    args = {}

    if device_type == 0:
        print('Sprinkler mit der ID ', device_id, ' gestoppt.')
        return redirect('/devices/?device=Sprinkler')
    if device_type == 1:
        print('Sensor mit der ID ', device_id, ' gestoppt.')
        return redirect('/devices/?device=Sensor')
    if device_type == 2:
        print('Pumpe mit der ID ', device_id, ' gestoppt.')
        return redirect('/devices/?device=Pumpe')

    return redirect('devices')



def device_edit(request, device_type, device_id):

    args = {}

    if device_type == 0:
        q = Sprinkler.objects.get(id=device_id)
    if device_type == 1:
        q = Sensor.objects.get(id=device_id)
    if device_type == 2:
        q = Pump.objects.get(id=device_id)

    args['device'] = q

    return TemplateResponse(request, "device_edit.html", args)

def device_delete(request, device_type, device_id):

    args = {}

    if device_type == 0:
        q = Sprinkler.objects.get(id=device_id).delete()
    if device_type == 1:
        q = Sensor.objects.get(id=device_id).delete()
    if device_type == 2:
        q = Pump.objects.get(id=device_id).delete()


    return redirect('devices')


def plans(request):

    args = {}

    # GET variables
    args['filter_name'] = request.GET.get('name', '')
    args['filter_status'] = request.GET.get('status', '')

    return TemplateResponse(request, "plans.html", args)

def statistics(request):
    template = loader.get_template("statistics.html")
    return HttpResponse(template.render())

def weather(request):
    template = loader.get_template("weather.html")
    return HttpResponse(template.render())

def settings(request):

    args = {}

    # GET variables
    args['filter_longitude'] = request.POST.get('longitude', '')
    args['filter_latitude'] = request.POST.get('latitude', '')

    # Argumente irgendwo hin speichern




    return TemplateResponse(request, "settings.html", args)

def help(request):
    template = loader.get_template("help.html")
    return HttpResponse(template.render())
