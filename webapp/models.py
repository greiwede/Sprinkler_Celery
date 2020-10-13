from django.db import models
from django.forms import ModelForm
from django import forms

import datetime

# Create your models here.

STATUS_CHOICES = [
        ('OK', 'OK'),
        ('Warnung', 'Warnung'),
        ('Fehler', 'Fehler'),
    ]

class Sprinkler(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    curr_active = models.BooleanField(default=False)
    device_type = 'Sprinkler'

    def __str__(self):
        return self.name

class SprinklerForm(ModelForm):
    class Meta:
        model = Sprinkler
        fields = ('name','status')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class Pump(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    curr_active = models.BooleanField(default=False)
    device_type = 'Pump'

    def __str__(self):
        return self.name

class PumpForm(ModelForm):
    class Meta:
        model = Pump
        fields = ('name','status')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class Sensor(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    curr_active = models.BooleanField(default=False)
    device_type = 'Sensor'

    def __str__(self):
        return self.name

class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = ('name','status')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class Plan(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    description = models.CharField(max_length=3000, default="Beschreibung")

    automation = models.BooleanField(default=False)

    # Relationen zu Sprinklern
    sprinkler = models.ManyToManyField(Sprinkler)

    # Relationen zu Pumpe
    pump = models.ManyToManyField(Pump)

    # Relation zu Sensoren
    sensor = models.ManyToManyField(Sensor)

    next_execution_time = None

    def __str__(self):
        return self.name

    def get_related_schedules(self):
        return self.schedule_set.all()
    
    def get_next_execution_date_time(self):
        next_execution_date_time = None
        schedules = self.get_related_schedules()

        for schedule in schedules:
            next_allow_date_time = schedule.get_next_allow_date_time()
            if next_execution_date_time == None:
                next_execution_date_time = next_allow_date_time
            elif next_execution_date_time > next_allow_date_time:
                next_execution_date_time = next_allow_date_time
        return next_execution_date_time

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ('name', 'status', 'description', 'automation', 'sprinkler', 'pump', 'sensor')
    
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'automation': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'sprinkler': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'pump': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'sensor': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
class Schedule(models.Model):

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    
    allow_monday = models.BooleanField(default=False)
    allow_tuesday = models.BooleanField(default=False)
    allow_wednesday = models.BooleanField(default=False)
    allow_thursday = models.BooleanField(default=False)
    allow_friday = models.BooleanField(default=False)
    allow_saturday = models.BooleanField(default=False)
    allow_sunday = models.BooleanField(default=False)
    allow_time_start = models.TimeField(auto_now=False, auto_now_add=False)
    allow_time_stop = models.TimeField(auto_now=False, auto_now_add=False)

    deny_monday = models.BooleanField(default=False)
    deny_tuesday = models.BooleanField(default=False)
    deny_wednesday = models.BooleanField(default=False)
    deny_thursday = models.BooleanField(default=False)
    deny_friday = models.BooleanField(default=False)
    deny_saturday = models.BooleanField(default=False)
    deny_sunday = models.BooleanField(default=False)
    deny_time_start = models.TimeField(auto_now=False, auto_now_add=False)
    deny_time_stop = models.TimeField(auto_now=False, auto_now_add=False)

    def get_next_execution_timestamp(self):
        nextAllowedWeekday = self.getNextAllowedDate()
    
    def get_next_allow_date_time(self):
        allowedWeekdays = self.get_allow_weekdays()
        weekday = datetime.datetime.now().weekday()

        for i in range(0, 8):
            if weekday in allowedWeekdays:
                now_date_time = datetime.datetime.now()
                temp_date_time = now_date_time + datetime.timedelta(days=i)

                day = str(temp_date_time.day)
                if int(day) < 10: day = str(0) + day

                month = str(temp_date_time.month)
                if int(month) < 10: month = str(0) + month

                year = str(temp_date_time.year)

                hour = str(self.allow_time_start.hour)
                if int(hour) < 10: hour = str(0) + hour

                minute = str(self.allow_time_start.minute)
                if int(minute) < 10: minute = str(0) + minute

                second = str(self.allow_time_start.second)
                if int(second) < 10: second = str(0) + second

                date_time_str = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second

                allow_date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                
                if allow_date_time > now_date_time:
                    return allow_date_time
            
            if weekday == 6:
                weekday = 0
            else:
                weekday += 1
    
    def get_allow_weekdays(self):
        allowedWeekdays = []
        if self.allow_monday: allowedWeekdays.append(0)
        if self.allow_tuesday: allowedWeekdays.append(1)
        if self.allow_wednesday: allowedWeekdays.append(2)
        if self.allow_thursday: allowedWeekdays.append(3)
        if self.allow_friday: allowedWeekdays.append(4)
        if self.allow_saturday: allowedWeekdays.append(5)
        if self.allow_sunday: allowedWeekdays.append(6)
        return allowedWeekdays




class ScheduleForm(ModelForm):

    class Meta:
        model = Schedule
        fields = ('plan', 'allow_monday', 'allow_tuesday', 'allow_wednesday', 'allow_thursday',
         'allow_friday', 'allow_saturday', 'allow_sunday', 'allow_time_start', 'allow_time_stop',
         'deny_monday', 'deny_tuesday', 'deny_wednesday', 'deny_thursday',
         'deny_friday', 'deny_saturday', 'deny_sunday', 'deny_time_start', 'deny_time_stop')


        widgets = {
            'plan': forms.NumberInput(attrs={'style': 'display:none'}), 
            'allow_monday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'allow_tuesday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'allow_wednesday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'allow_thursday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_friday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'allow_saturday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'allow_sunday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'allow_time_start': forms.TimeInput(attrs={'class': 'form-control'}), 
            'allow_time_stop': forms.TimeInput(attrs={'class': 'form-control'}),
            'deny_monday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'deny_tuesday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'deny_wednesday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'deny_thursday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_friday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'deny_saturday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'deny_sunday': forms.CheckboxInput(attrs={'class': 'form-control'}), 
            'deny_time_start': forms.TimeInput(attrs={'class': 'form-control'}), 
            'deny_time_stop': forms.TimeInput(attrs={'class': 'form-control'}),
        }

