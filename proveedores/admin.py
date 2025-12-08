# administrador/views.py
from django.shortcuts import render, redirect, get_object_or_404
from proveedores.models import Producto
from django.contrib.auth.models import User

def asignar_producto(request, producto_id, vendedor_id):
    producto = get_object_or_404(Producto, id=producto_id)
    vendedor = get_object_or_404(User, id=vendedor_id)
    producto.asignado_a = vendedor
    producto.save()
    return redirect("administrador:index")
