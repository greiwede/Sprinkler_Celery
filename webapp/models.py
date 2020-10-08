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
    plan_name = models.CharField(max_length=200)
    device_status = models.CharField(max_length=200)