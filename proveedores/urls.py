from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "proveedores"

urlpatterns = [
    # Dashboard del proveedor
    path("dashboard/", views.dashboard_proveedor, name="dashboard"),

    # Agregar producto nuevo
    path("agregar/", views.agregar_producto_proveedor, name="agregar_producto_proveedor"),

    # Vista para administrador
    path("admin/listar/", views.listado_productos_admin, name="listado_productos_admin"),
    path('editar/<int:pk>/', views.editar_producto_view, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),
    path('listado_admin/', views.listado_productos_admin, name='listado_productos_admin'),
]
