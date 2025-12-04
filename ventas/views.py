from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Venta, DetalleVenta
from .forms import DetalleVentaForm, VentaForm
from productos.models import Producto
import json
from decimal import Decimal

@login_required
def punto_venta(request):
    """Vista principal del punto de venta"""
    productos = Producto.objects.filter(activo=True, stock__gt=0)
    
    # Crear una nueva venta vacía si no hay una en sesión
    if 'venta_actual' not in request.session:
        venta = Venta.objects.create()
        request.session['venta_actual'] = venta.id
    else:
        venta_id = request.session['venta_actual']
        venta = get_object_or_404(Venta, id=venta_id)
    
    detalles = venta.detalles.all()
    form_detalle = DetalleVentaForm()
    form_venta = VentaForm(instance=venta)
    
    context = {
        'productos': productos,
        'venta': venta,
        'detalles': detalles,
        'form_detalle': form_detalle,
        'form_venta': form_venta,
    }
    
    return render(request, 'ventas/punto_venta.html', context)

@login_required
@require_POST
def agregar_producto(request):
    """Agrega un producto a la venta actual"""
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    
    venta_id = request.session.get('venta_actual')
    if not venta_id:
        return JsonResponse({'error': 'No hay venta activa'}, status=400)
    
    venta = get_object_or_404(Venta, id=venta_id)
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verificar stock disponible
    if producto.stock < cantidad:
        return JsonResponse({
            'error': f'Stock insuficiente. Disponible: {producto.stock}'
        }, status=400)
    
    # Verificar si el producto ya está en la venta
    detalle_existente = venta.detalles.filter(producto=producto).first()
    
    if detalle_existente:
        # Actualizar cantidad
        detalle_existente.cantidad += cantidad
        detalle_existente.calcular_subtotal()
    else:
        # Crear nuevo detalle
        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio_venta
        )
    
    # Recalcular total
    venta.calcular_total()
    
    return JsonResponse({
        'success': True,
        'total': str(venta.total),
        'items_count': venta.detalles.count()
    })

@login_required
@require_POST
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
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'total': str(venta.total),
            'items_count': venta.detalles.count()
        })
    
    return redirect('punto_venta')

@login_required
@require_POST
def finalizar_venta(request):
    """Finaliza la venta actual y procesa el pago"""
    venta_id = request.session.get('venta_actual')
    if not venta_id:
        return JsonResponse({'error': 'No hay venta activa'}, status=400)
    
    venta = get_object_or_404(Venta, id=venta_id)
    
    # Verificar que haya productos en la venta
    if venta.detalles.count() == 0:
        return JsonResponse({'error': 'No hay productos en la venta'}, status=400)
    
    # Procesar pago
    paga_con = Decimal(request.POST.get('paga_con', 0))
    
    if paga_con < venta.total:
        return JsonResponse({
            'error': f'Pago insuficiente. Total: {venta.total}'
        }, status=400)
    
    venta.paga_con = paga_con
    venta.calcular_cambio()
    venta.completada = True
    venta.save()
    
    # Generar ticket (aquí puedes implementar la lógica para imprimir)
    
    # Limpiar venta de la sesión
    if 'venta_actual' in request.session:
        del request.session['venta_actual']
    
    return JsonResponse({
        'success': True,
        'venta_id': venta.id,
        'total': str(venta.total),
        'paga_con': str(venta.paga_con),
        'cambio': str(venta.cambio)
    })

@login_required
def cancelar_venta(request):
    """Cancela la venta actual y restaura el stock"""
    venta_id = request.session.get('venta_actual')
    if venta_id:
        venta = get_object_or_404(Venta, id=venta_id)
        
        # Restaurar stock de todos los productos
        for detalle in venta.detalles.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        
        # Eliminar la venta
        venta.delete()
    
    # Limpiar venta de la sesión
    if 'venta_actual' in request.session:
        del request.session['venta_actual']
    
    return redirect('punto_venta')

@login_required
def historial_ventas(request):
    """Muestra el historial de ventas"""
    ventas = Venta.objects.filter(completada=True).order_by('-fecha_hora')
    
    # Filtros
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if fecha_desde:
        ventas = ventas.filter(fecha_hora__date__gte=fecha_desde)
    if fecha_hasta:
        ventas = ventas.filter(fecha_hora__date__lte=fecha_hasta)
    
    total_ventas = sum(venta.total for venta in ventas)
    
    context = {
        'ventas': ventas,
        'total_ventas': total_ventas,
    }
    
    return render(request, 'ventas/historial.html', context)

@login_required
def detalle_venta(request, venta_id):
    """Muestra el detalle de una venta específica"""
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all()
    
    context = {
        'venta': venta,
        'detalles': detalles,
    }
    
    return render(request, 'ventas/detalle_venta.html', context)