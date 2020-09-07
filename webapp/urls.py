from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('devices/', views.devices, name='devices'),
    path('plans/', views.plans, name='plans'),
    path('statistics/', views.statistics, name='statistics'),
    path('weather/', views.weather, name='weather'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
    path('admin/', admin.site.urls),
]