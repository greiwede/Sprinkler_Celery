from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('devices/', views.devices, name='devices'),
    path('devices/start/<int:device_type>/<int:device_id>', views.device_start, name='device_start'),
    path('devices/stop/<int:device_type>/<int:device_id>', views.device_stop, name='device_stop'),
    
    path('devices/create/<int:device_type>', views.device_create, name='device_create'),
    path('devices/edit/<int:device_type>/<int:device_id>', views.device_edit, name='device_edit'),
    path('devices/delete/<int:device_type>/<int:device_id>', views.device_delete, name='device_delete'),
    
    path('plans/', views.plans, name='plans'),
    path('plans/create', views.plans_create, name='plan_create'),

    path('plans/edit/<int:plan_id>', views.plans_edit, name='plan_edit'),
    path('plans/delete/<int:plan_id>', views.plans_delete, name='plan_delete'),

    path('statistics/', views.statistics, name='statistics'),
    path('weather/', views.weather, name='weather'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
    path('admin/', admin.site.urls),
]