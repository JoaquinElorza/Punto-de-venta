from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Venta, DetalleVenta
from productos.models import Producto
from decimal import Decimal

@login_required
def punto_venta(request):
    """Vista principal del punto de venta"""
    productos = Producto.objects.filter(activo=True, stock__gt=0)
    
    # Obtener o crear venta activa
    venta_activa = Venta.objects.filter(completada=False).last()
    if not venta_activa:
        venta_activa = Venta.objects.create()
    
    detalles = venta_activa.detalles.all()
    
    context = {
        'productos': productos,
        'venta': venta_activa,
        'detalles': detalles,
    }
    return render(request, 'ventas/punto_venta.html', context)

@login_required
def agregar_producto(request, producto_id):
    """Agrega un producto a la venta actual"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtener venta activa
    venta_activa = Venta.objects.filter(completada=False).last()
    if not venta_activa:
        venta_activa = Venta.objects.create()
    
    # Verificar si el producto ya está en la venta
    detalle_existente = venta_activa.detalles.filter(producto=producto).first()
    
    if detalle_existente:
        # Incrementar cantidad
        detalle_existente.cantidad += 1
        detalle_existente.save()
    else:
        # Crear nuevo detalle
        DetalleVenta.objects.create(
            venta=venta_activa,
            producto=producto,
            cantidad=1,
            precio_unitario=producto.precio
        )
    
    return redirect('ventas:punto_venta')

@login_required
def eliminar_detalle(request, detalle_id):
    """Elimina un detalle de la venta"""
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    venta = detalle.venta
    
    # Restaurar stock del producto
    producto = detalle.producto
    producto.stock += detalle.cantidad
    producto.save()
    
    # Eliminar detalle
    detalle.delete()
    
    # Recalcular total
    venta.calcular_total()
    
    return redirect('ventas:punto_venta')

@login_required
def finalizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        paga_con = Decimal(request.POST.get('paga_con', '0'))
        
        if paga_con >= venta.total:
            venta.paga_con = paga_con
            venta.completada = True
            venta.calcular_cambio()
            venta.save()
            
            return render(request, 'ventas/ticket.html', {'venta': venta})
    
    return redirect('ventas:punto_venta')

@login_required
def cancelar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    # Restaurar stock de todos los productos
    for detalle in venta.detalles.all():
        producto = detalle.producto
        producto.stock += detalle.cantidad
        producto.save()
    
    venta.delete()
    return redirect('ventas:punto_venta')

@login_required
def historial_ventas(request):
    ventas = Venta.objects.filter(completada=True).order_by('-fecha_hora')
    return render(request, 'ventas/historial.html', {'ventas': ventas})