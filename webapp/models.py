from django.db import models

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

class Pump(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    curr_active = models.BooleanField(default=False)
    device_type = 'Pump'


class Sensor(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )
    curr_active = models.BooleanField(default=False)
    device_type = 'Sensor'

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

    # Relationen zu Pumpe

    # Relation zu Sensoren

    # Relation zu den Schedules

    
class Schedule(models.Model):

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    
    allow_monday = models.BooleanField(default=False)
    allow_tuesday = models.BooleanField(default=False)
    allow_wednesday = models.BooleanField(default=False)
    allow_thursday = models.BooleanField(default=False)
    allow_friday = models.BooleanField(default=False)
    allow_saturday = models.BooleanField(default=False)
    allow_sunday = models.BooleanField(default=False)
    allow_time_start = models.TimeField(auto_now=True, auto_now_add=False)
    allow_time_stop = models.TimeField(auto_now=True, auto_now_add=False)

    deny_monday = models.BooleanField(default=False)
    deny_tuesday = models.BooleanField(default=False)
    deny_wednesday = models.BooleanField(default=False)
    deny_thursday = models.BooleanField(default=False)
    deny_friday = models.BooleanField(default=False)
    deny_saturday = models.BooleanField(default=False)
    deny_sunday = models.BooleanField(default=False)
    deny_time_start = models.TimeField(auto_now=True, auto_now_add=False)
    deny_time_stop = models.TimeField(auto_now=True, auto_now_add=False)