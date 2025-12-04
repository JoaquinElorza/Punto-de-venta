from django.urls import path
from . import views
from django.shortcuts import render
from django.contrib.auth import views as auth_views

app_name = 'administrador'

def index(request):
    return render(request, 'administrador/index.html')

urlpatterns = [
    path('', views.index, name='index'),  # Panel principal
    path('ventas/', views.ventas_historial, name='ventas_historial'),
    path('reportes/', views.reportes, name='reportes'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]




