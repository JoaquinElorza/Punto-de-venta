from django.urls import path
from . import views
from django.shortcuts import render

app_name = 'administrador'

def index(request):
    return render(request, 'administrador/index.html')

urlpatterns = [
    path('', views.index, name='index'),  # Panel principal
    path('ventas/', views.ventas_historial, name='ventas_historial'),
    path('reportes/', views.reportes, name='reportes'),
]




