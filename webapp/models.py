from django.db import models

# Create your models here.

class Device(models.Model):
    device_name = models.CharField(max_length=200)
    device_type = models.CharField(max_length=200)
    device_status = models.CharField(max_length=200)

class Plan(models.Model):
    plan_name = models.CharField(max_length=200)
    device_status = models.CharField(max_length=200)