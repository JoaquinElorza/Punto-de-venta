from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.punto_venta, name='punto_venta'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('eliminar-detalle/<int:detalle_id>/', views.eliminar_detalle, name='eliminar_detalle'),
    path('finalizar-venta/', views.finalizar_venta, name='finalizar_venta'),
    path('cancelar-venta/', views.cancelar_venta, name='cancelar_venta'),
    path('historial/', views.historial_ventas, name='historial_ventas'),
    path('detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
]