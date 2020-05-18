# Added by Anant Dev
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('extrapolate/<country_name>', views.extrapolate, name = 'extrapolate'),
    path('compare', views.compare, name = 'compare'),
    path('analyze', views.analyze, name = 'analyze'),
    path('alerts', views.alerts, name = 'alerts')
]
