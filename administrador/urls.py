from django.urls import path
from . import views
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from proveedores import views as proveedor_views
from proveedores.views import dashboard_proveedor


app_name = 'administrador'

def index(request):
    return render(request, 'administrador/index.html')

urlpatterns = [
    path('', views.index, name='index'), 
    path('ventas/', views.ventas_historial, name='ventas_historial'),
    path("productos/", views.dashboard_productos_admin, name="dashboard_productos"),
    path('reportes/', views.reportes, name='reportes'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("asignar-producto/<int:producto_id>/", views.asignar_producto, name="asignar_producto"),
    path("quitar-producto/<int:producto_id>/", views.quitar_asignacion_producto, name="quitar_producto"),
    path("productos/", dashboard_proveedor, name="dashboard_productos"),
    path("reportes/", views.reportes, name="reportes"),
    path("ver-productos/", views.ver_productos, name="ver_productos"),


    
]



