from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context, loader
from django.template.response import TemplateResponse
from django.forms import inlineformset_factory

import json

from .models import *

# Create your views here.

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def dashboard(request):

    args = {}

    # Read user config from config file
    with open('user_settings.json', 'r') as f:
            user_config = json.load(f)

    if user_config['userName'] != '':
        args['name'] = user_config['userName']
    else:
        args['name'] = 'Honey'
    



    return TemplateResponse(request, "dashboard.html", args)

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
        t = Sprinkler.objects.get(id=device_id)
        t.curr_active = True
        t.save()
        print('Sprinkler mit der ID ', device_id, ' gestartet.')
        return redirect('/devices/?device=Sprinkler')
    if device_type == 1:
        t = Sensor.objects.get(id=device_id)
        t.curr_active = True
        t.save()
        print('Sensor mit der ID ', device_id, ' gestartet.')
        return redirect('/devices/?device=Sensor')
    if device_type == 2:
        t = Pump.objects.get(id=device_id)
        t.curr_active = True
        t.save()
        print('Pumpe mit der ID ', device_id, ' gestartet.')
        return redirect('/devices/?device=Pumpe')

    

    return redirect('devices')

def device_stop(request, device_type, device_id):

    args = {}

    if device_type == 0:
        t = Sprinkler.objects.get(id=device_id)
        t.curr_active = False
        t.save()
        print('Sprinkler mit der ID ', device_id, ' gestoppt.')
        return redirect('/devices/?device=Sprinkler')
    if device_type == 1:
        t = Sensor.objects.get(id=device_id)
        t.curr_active = False
        t.save()
        print('Sensor mit der ID ', device_id, ' gestoppt.')
        return redirect('/devices/?device=Sensor')
    if device_type == 2:
        t = Pump.objects.get(id=device_id)
        t.curr_active = False
        t.save()
        print('Pumpe mit der ID ', device_id, ' gestoppt.')
        return redirect('/devices/?device=Pumpe')

    return redirect('devices')

def device_create(request, device_type):

    args = {}

    args['device_type'] = device_type

    if device_type == 0: # Sprinkler
        if request.method == 'POST':
            d = SprinklerForm(request.POST)
            new_device = d.save()
            return redirect('devices')
        else:
            args['headline'] = "Neuer Sprinkler"
            args['form'] = SprinklerForm()
    if device_type == 1: # Sensor
        if request.method == 'POST':
            d = SensorForm(request.POST)
            new_device = d.save()
            return redirect('/devices/?device=Sensor')
        else:
            args['headline'] = "Neuer Sensor"
            args['form'] = SensorForm()
    if device_type == 2: # Pump
        if request.method == 'POST':
            d = PumpForm(request.POST)
            new_device = d.save()
            return redirect('/devices/?device=Pumpe')
        else:
            args['headline'] = "Neue Pumpe"
            args['form'] = PumpForm()

    

    return TemplateResponse(request, "device_create.html", args)

def device_edit(request, device_type, device_id):

    args = {}

    args['device_type'] = device_type

    args['device_id'] = device_id

    if device_type == 0: # Sprinkler

        if request.method == 'POST':

            d = Sprinkler.objects.get(pk=device_id)
            f = SprinklerForm(request.POST, instance=d)
            f.save()
            return redirect('devices')

        else:

            d = Sprinkler.objects.get(pk=device_id)
            args['headline'] = "Sprinkler bearbeiten"
            args['form'] = SprinklerForm(instance=d)
        
    if device_type == 1: # Sensor

        if request.method == 'POST':

            d = Sensor.objects.get(pk=device_id)
            f = SensorForm(request.POST, instance=d)
            f.save()
            return redirect('/devices/?device=Sensor')

        else:

            d = Sensor.objects.get(pk=device_id)
            args['headline'] = "Sensor bearbeiten"
            args['form'] = SensorForm(instance=d)
        
    if device_type == 2: # Pump

        if request.method == 'POST':

            d = Pump.objects.get(pk=device_id)
            f = PumpForm(request.POST, instance=d)
            f.save()
            return redirect('/devices/?device=Pumpe')

        else:

            d = Pump.objects.get(pk=device_id)
            args['headline'] = "Pumpe bearbeiten"
            args['form'] = PumpForm(instance=d)
        

    

    return TemplateResponse(request, "device_edit.html", args)

def device_delete(request, device_type, device_id):

    args = {}

    if device_type == 0:
        q = Sprinkler.objects.get(id=device_id).delete()
    if device_type == 1:
        q = Sensor.objects.get(id=device_id).delete()
        return redirect('/devices/?device=Sensor')
    if device_type == 2:
        q = Pump.objects.get(id=device_id).delete()
        return redirect('/devices/?device=Pumpe')


    return redirect('devices')


def plans(request):

    args = {}

    args['filter_name'] = request.GET.get('name', '')
    args['filter_status'] = request.GET.get('status', '')

    q = Plan.objects

    check = 0

    if(args['filter_name']!=''):
        q = q.filter(name__contains=args['filter_name'])
        check = 1
    if(args['filter_status'] == 'OK' or args['filter_status'] == 'Warnung' or args['filter_status'] == 'Fehler'):
        q = q.filter(status__contains=args['filter_status'])
        check = 1

    if(check == 0):
        q = q.all()

    # schedules = q.get(pk=1).get_related_schedules()
    # for schedule in schedules:
    #     print(schedule.__str__())
    #     print(schedule.get_next_allow_date())

    for plan in q:
        plan.next_execution_time = plan.get_next_execution_date_time()

    args['plans'] = q

    return TemplateResponse(request, "plans.html", args)

def plans_create(request):

    args = {}

    args['form'] = PlanForm()

    if request.method == 'POST':
        f = PlanForm(request.POST)
        new_plan = f.save()
        return redirect('plans')

    return TemplateResponse(request, "plans_create.html", args)

def plans_edit(request, plan_id):

    args = {}

    args['id'] = plan_id

    if request.method == 'POST':

        p = Plan.objects.get(pk=plan_id)
        f = PlanForm(request.POST, instance=p)
        f.save()
        return redirect('plans')

    else:

        plan = Plan.objects.get(pk=plan_id)
        args['form'] = PlanForm(instance=plan)

        args['schedules'] = Schedule.objects.filter(plan=plan_id).all()

        

    return TemplateResponse(request, "plans_edit.html", args)

def plans_delete(request, plan_id):

    instance = Plan.objects.get(id=plan_id)
    instance.delete()

    return redirect('plans')

def schedule_create(request, plan_id):

    args = {}

    args['form'] = ScheduleForm(initial={'plan': plan_id})

    args['plan'] = Plan.objects.get(pk=plan_id)

    if request.method == 'POST':
        s = ScheduleForm(request.POST)
        new_schedule = s.save()
        return redirect('plan_edit', plan_id=plan_id)

    return TemplateResponse(request, "schedule_create.html", args)


    return redirect('plan_edit', plan_id=plan_id)

def schedule_edit(request, plan_id, schedule_id):

    args = {}

    args['id'] = plan_id

    args['plan'] = Plan.objects.get(pk=plan_id)

    args['schedule_id'] = schedule_id

    if request.method == 'POST':

        s = Schedule.objects.get(pk=schedule_id)
        f = ScheduleForm(request.POST, instance=s)
        f.save()
        return redirect('plan_edit', plan_id=plan_id)

    else:

        schedule = Schedule.objects.get(pk=schedule_id)
        args['form'] = ScheduleForm(instance=schedule)

        

    return TemplateResponse(request, "schedule_edit.html", args)

    

def schedule_delete(request, plan_id, schedule_id):

    Schedule.objects.filter(id=schedule_id, plan=plan_id).delete()

    return redirect('plan_edit', plan_id=plan_id)


def statistics(request):
    template = loader.get_template("statistics.html")
    return HttpResponse(template.render())

def weather(request):
    template = loader.get_template("weather.html")
    return HttpResponse(template.render())

def settings(request):
    
    # Read user config from config file
    with open('user_settings.json', 'r') as f:
            user_config = json.load(f)

    args = dict()

    # GET variables
    args['filter_user_name'] = request.POST.get('userName', user_config['userName'])
    args['filter_latitude'] = request.POST.get('latitude', user_config['latitude'])
    args['filter_longitude'] = request.POST.get('longitude', user_config['longitude'])
    args['filter_owm_api_key'] = request.POST.get('owmAPIKey', user_config['owmAPIKey'])

    user_config = {
                    'userName': args['filter_user_name'], 
                    'latitude': args['filter_latitude'],
                    'longitude': args['filter_longitude'],
                    'owmAPIKey': args['filter_owm_api_key'],
                  }

    # Save user configuration to config file
    with open('user_settings.json', 'w') as f:
        json.dump(user_config, f, indent=4)

    return TemplateResponse(request, "settings.html", args)

def help(request):
    template = loader.get_template("help.html")
    return HttpResponse(template.render())
