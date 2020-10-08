from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Sprinkler)

admin.site.register(Pump)

admin.site.register(Sensor)

admin.site.register(Plan)

admin.site.register(Schedule)


