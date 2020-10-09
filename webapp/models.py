from django.db import models
from django.forms import ModelForm

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

class Plan(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    description = models.CharField(max_length=3000, default="Beschreibung")

    automation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


    # Relationen zu Sprinklern
    sprinkler = models.ManyToManyField(Sprinkler)

    # Relationen zu Pumpe
    pump = models.ManyToManyField(Pump)

    # Relation zu Sensoren
    sensor = models.ManyToManyField(Sensor)


    # Form


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'status', 'description', 'automation', 'sprinkler', 'pump', 'sensor']



    
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