from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from proveedores.models import Producto
from ventas.models import Venta
from django.contrib.auth import get_user_model

from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
from ventas.models import Venta, DetalleVenta
from django.contrib.auth.models import User

User = get_user_model()

@staff_member_required
def dashboard_productos_admin(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')  
    return render(request, "proveedores/dashboard.html", {"productos": productos})

@staff_member_required
def index(request):
    productos_count = Producto.objects.count()
    ventas_total = Venta.objects.count()
    ventas_recientes = Venta.objects.order_by('-fecha_hora')[:5]
    productos_recientes = Producto.objects.order_by('-fecha_creacion')[:10]  

    context = {
        'productos_count': productos_count,
        'ventas_total': ventas_total,
        'ventas_recientes': ventas_recientes,
        'productos_recientes': productos_recientes,
    }
    return render(request, 'administrador/index.html', context)

@staff_member_required
def ventas_historial(request):
    ventas = Venta.objects.order_by('-fecha_hora')
    return render(request, 'administrador/ventas_historial.html', {'ventas': ventas})

@staff_member_required
def reportes(request):
    return render(request, 'administrador/reportes.html')

@staff_member_required
def reportes(request):

    # ---------- 1. Ventas por día ----------
    hoy = now().date()
    ventas_dia = Venta.objects.filter(fecha_hora__date=hoy)\
                              .aggregate(total=Sum('total'))['total'] or 0

    # ---------- 2. Ventas por mes ----------
    mes_actual = now().month
    ventas_mes = Venta.objects.filter(fecha_hora__month=mes_actual)\
                              .aggregate(total=Sum('total'))['total'] or 0

    # ---------- 3. Productos más vendidos ----------
    productos_populares = (
        DetalleVenta.objects
        .values('producto__nombre')
        .annotate(total_vendidos=Sum('cantidad'))
        .order_by('-total_vendidos')[:5]
    )

    # ---------- 4. Productos con stock bajo ----------
    stock_bajo = Producto.objects.filter(stock__lte=5).order_by('stock')[:10]

    # ---------- 5. Ingresos totales ----------
    ingresos_totales = Venta.objects.aggregate(total=Sum('total'))['total'] or 0

    # ---------- 6. Rendimiento por vendedor ----------
    rendimiento_vendedores = (
        Venta.objects.values('vendedor__username')
        .annotate(total=Sum('total'))
        .order_by('-total')
    )

    context = {
        "ventas_dia": ventas_dia,
        "ventas_mes": ventas_mes,
        "productos_populares": productos_populares,
        "stock_bajo": stock_bajo,
        "ingresos_totales": ingresos_totales,
        "rendimiento_vendedores": rendimiento_vendedores,
    }

    return render(request, "administrador/reportes.html", context)

@staff_member_required


def ver_productos(request):
    productos = Producto.objects.all().order_by("nombre")
    return render(request, "administrador/verproductos.html", {"productos": productos})


@staff_member_required
def asignar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    vendedores = User.objects.filter(is_staff=False)

    if request.method == "POST":
        vendedor_id = request.POST.get("vendedor_id")
        vendedor = get_object_or_404(User, id=vendedor_id)
        producto.asignado_a = vendedor
        producto.save()
        return redirect("administrador:index")

    return render(request, "administrador/asignar_producto.html", {
        "producto": producto,
        "vendedores": vendedores
    })


@staff_member_required
def quitar_asignacion_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.asignado_a = None
        producto.save()
    return redirect("administrador:index")
