from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.punto_venta, name='punto_venta'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('eliminar/<int:detalle_id>/', views.eliminar_detalle, name='eliminar_detalle'),
    path('finalizar/<int:venta_id>/', views.finalizar_venta, name='finalizar_venta'),
    path('cancelar/<int:venta_id>/', views.cancelar_venta, name='cancelar_venta'),
]