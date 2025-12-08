from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Venta, DetalleVenta
from proveedores.models import Producto
from django.db.models import Q

@login_required
def punto_venta(request):
    # 🔍 texto de búsqueda
    termino = request.GET.get("q", "").strip()

    # Solo productos activos, con stock y asignados a este vendedor
    productos = Producto.objects.filter(
        activo=True,
        stock__gt=0,
        asignado_a=request.user
    )

    # Si hay búsqueda, filtramos por nombre o descripción
    if termino:
        productos = productos.filter(
            Q(nombre__icontains=termino) |
            Q(descripcion__icontains=termino)
        )

    # Venta activa por vendedor
    venta_activa = Venta.objects.filter(completada=False, vendedor=request.user).last()
    if not venta_activa:
        venta_activa = Venta.objects.create(vendedor=request.user)

    context = {
        "productos": productos,
        "venta": venta_activa,
        "detalles": venta_activa.detalles.all(),
        "termino": termino,  # 👉 para rellenar el input
    }
    return render(request, "ventas/punto_venta.html", context)

@login_required
def agregar_producto(request, producto_id):
    # Obtener instancia de Producto (no usar nombre, debe ser la instancia)
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    if producto.stock <= 0:
        return redirect('ventas:punto_venta')

    venta_activa = Venta.objects.filter(completada=False, vendedor=request.user).last()
    if not venta_activa:
        venta_activa = Venta.objects.create(vendedor=request.user)

    # Buscar si ya existe detalle para este producto usando la instancia
    detalle_existente = venta_activa.detalles.filter(producto=producto).first()


    if detalle_existente:
        if producto.stock >= detalle_existente.cantidad + 1:
            detalle_existente.cantidad += 1
            detalle_existente.save()
    else:
        DetalleVenta.objects.create(
            venta=venta_activa,
            producto=producto,           
            cantidad=1,
            precio_unitario=producto.precio
        )

    venta_activa.calcular_total()
    venta_activa.save()

    return redirect('ventas:punto_venta')


@login_required
def eliminar_detalle(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    venta = detalle.venta

    # Restaurar stock del producto
    producto = detalle.producto
    producto.stock += detalle.cantidad
    producto.save()

    # Eliminar detalle y recalcular total
    detalle.delete()
    venta.calcular_total()
    venta.save()

    return redirect('ventas:punto_venta')

@login_required
def finalizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, vendedor=request.user)

    if request.method == 'POST':
        paga_con_raw = request.POST.get('paga_con', '')
        try:
            paga_con = Decimal(paga_con_raw)
        except Exception:
            return redirect('ventas:punto_venta')

        # Validar que cubre el total
        if paga_con >= venta.total:
            venta.paga_con = paga_con
            venta.completada = True
            venta.calcular_cambio()
            venta.save()
            return render(request, 'ventas/ticket.html', {'venta': venta})

    return redirect('ventas:punto_venta')

@login_required
def cancelar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, vendedor=request.user)

    # Restaurar stock de todos los productos del carrito
    for detalle in venta.detalles.all():
        producto = detalle.producto
        producto.stock += detalle.cantidad
        producto.save()

    # Eliminar la venta
    venta.delete()
    return redirect('ventas:punto_venta')

@login_required
def historial_ventas(request):
    ventas = Venta.objects.filter(
        completada=True,
        vendedor=request.user
    ).order_by('-fecha_hora')
    return render(request, 'ventas/historial.html', {'ventas': ventas})
