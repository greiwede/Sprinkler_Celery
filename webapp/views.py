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
        devices = Pump.objects
        args['edit_key'] = 2
        args['type_name'] = 'pump'

    elif args['filter_device'] == 'Sensor':
        devices = Sensor.objects
        args['edit_key'] = 1
        args['type_name'] = 'sensor'

    elif args['filter_device'] == 'Sprinkler':
        devices = Sprinkler.objects
        args['edit_key'] = 0
        args['type_name'] = 'sprinkler'
    
    elif args['filter_device'] == '':
        devices = Sprinkler.objects
        args['edit_key'] = 0
        args['filter_device'] = 'Sprinkler'
        args['type_name'] = 'sprinkler'

    if args['filter_name'] != '':
        devices = devices.filter(name__contains=args['filter_name'])
        check = 1
    if args['filter_status'] == 'OK' or args['filter_status'] == 'Warnung' or args['filter_status'] == 'Fehler':
        devices = devices.filter(status__contains=args['filter_status'])
        check = 1

    if(check == 0):
        devices = devices.all()

    args['devices'] = devices

    return TemplateResponse(request, "devices.html", args)

def device_start(request, device_type, device_id):
    args = {}

    if device_type == 0:
        sprinklers = Sprinkler.objects.get(id=device_id)
        sprinklers.curr_active = True
        sprinklers.save()
        print('Sprinkler mit der ID ', device_id, ' wurde gestartet.')
        return redirect('/devices/?device=Sprinkler')
    elif device_type == 1:
        sensors = Sensor.objects.get(id=device_id)
        sensors.curr_active = True
        sensors.save()
        print('Sensor mit der ID ', device_id, ' wurde gestartet.')
        return redirect('/devices/?device=Sensor')
    elif device_type == 2:
        pumps = Pump.objects.get(id=device_id)
        pumps.curr_active = True
        pumps.save()
        print('Pumpe mit der ID ', device_id, ' wurde gestartet.')
        return redirect('/devices/?device=Pumpe')

    return redirect('devices')

def device_stop(request, device_type, device_id):
    args = {}

    if device_type == 0:
        sprinklers = Sprinkler.objects.get(id=device_id)
        sprinklers.curr_active = False
        sprinklers.save()
        print('Sprinkler mit der ID ', device_id, ' wurde gestoppt.')
        return redirect('/devices/?device=Sprinkler')
    elif device_type == 1:
        sensors = Sensor.objects.get(id=device_id)
        sensors.curr_active = False
        sensors.save()
        print('Sensor mit der ID ', device_id, ' wurde gestoppt.')
        return redirect('/devices/?device=Sensor')
    elif device_type == 2:
        pumps = Pump.objects.get(id=device_id)
        pumps.curr_active = False
        pumps.save()
        print('Pumpe mit der ID ', device_id, ' wurde gestoppt.')
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
    elif device_type == 1: # Sensor
        if request.method == 'POST':
            d = SensorForm(request.POST)
            new_device = d.save()
            return redirect('/devices/?device=Sensor')
        else:
            args['headline'] = "Neuer Sensor"
            args['form'] = SensorForm()
    elif device_type == 2: # Pump
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
        
    elif device_type == 1: # Sensor
        if request.method == 'POST':
            d = Sensor.objects.get(pk=device_id)
            f = SensorForm(request.POST, instance=d)
            f.save()
            return redirect('/devices/?device=Sensor')
        else:
            d = Sensor.objects.get(pk=device_id)
            args['headline'] = "Sensor bearbeiten"
            args['form'] = SensorForm(instance=d)
        
    elif device_type == 2: # Pump
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
        Sprinkler.objects.get(id=device_id).delete()
        return redirect('/devices/?device=Sprinkler')
    elif device_type == 1:
        Sensor.objects.get(id=device_id).delete()
        return redirect('/devices/?device=Sensor')
    elif device_type == 2:
        Pump.objects.get(id=device_id).delete()
        return redirect('/devices/?device=Pumpe')

    return redirect('devices')

def plans(request):
    args = {}
    args['filter_name'] = request.GET.get('name', '')
    args['filter_status'] = request.GET.get('status', '')

    plans = Plan.objects

    check = 0

    if(args['filter_name'] != ''):
        plans = plans.filter(name__contains=args['filter_name'])
        check = 1
    elif(args['filter_status'] == 'OK' or args['filter_status'] == 'Warnung' or args['filter_status'] == 'Fehler'):
        plans = plans.filter(status__contains=args['filter_status'])
        check = 1

    if(check == 0):
        plans = plans.all()

    for plan in plans:
        plan.next_execution_time = plan.get_next_allowed_start_date_time()

    args['plans'] = plans

    return TemplateResponse(request, "plans.html", args)

def plans_create(request):
    args = {}
    args['form'] = PlanForm()

    if request.method == 'POST':
        plan_form = PlanForm(request.POST)
        new_plan = plan_form.save()
        return redirect('plans')

    return TemplateResponse(request, "plans_create.html", args)

def plans_edit(request, plan_id):
    args = {}
    args['id'] = plan_id

    if request.method == 'POST':
        plan = Plan.objects.get(pk=plan_id)
        plan_form = PlanForm(request.POST, instance=plan)
        plan_form.save()
        return redirect('plans')
    else:
        plan = Plan.objects.get(pk=plan_id)
        args['form'] = PlanForm(instance=plan)

        schedules = Schedule.objects.filter(plan=plan_id).all()
        for schedule in schedules:
            schedule.allowed_weekdays = schedule.get_allowed_weekdays()
            schedule.denied_weekdays = schedule.get_denied_weekdays()
            next_allowed_start_date_time = schedule.get_next_date_time(schedule.allowed_weekdays, schedule.allow_time_start)
            next_allowed_end_date_time = schedule.get_next_date_time(schedule.allowed_weekdays, schedule.allow_time_stop)
            next_denied_start_date_time = schedule.get_next_date_time(schedule.denied_weekdays, schedule.deny_time_start)
            next_denied_end_date_time = schedule.get_next_date_time(schedule.denied_weekdays, schedule.deny_time_stop)

        args['schedules'] = schedules

    return TemplateResponse(request, "plans_edit.html", args)

def plans_delete(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.delete()

    return redirect('plans')

def schedule_create(request, plan_id):
    args = {}
    args['form'] = ScheduleForm(initial={'plan': plan_id})
    args['plan'] = Plan.objects.get(pk=plan_id)

    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        new_schedule = schedule_form.save()
        return redirect('plan_edit', plan_id=plan_id)

    return TemplateResponse(request, "schedule_create.html", args)


    return redirect('plan_edit', plan_id=plan_id) # Lennart?

def schedule_edit(request, plan_id, schedule_id):
    args = {}
    args['id'] = plan_id
    args['plan'] = Plan.objects.get(pk=plan_id)
    args['schedule_id'] = schedule_id

    if request.method == 'POST':
        schedule = Schedule.objects.get(pk=schedule_id)
        schedule_form = ScheduleForm(request.POST, instance=schedule)
        schedule_form.save()
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

    args = {}

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