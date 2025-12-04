from django.shortcuts import render
from productos.models import Producto

def index(request):
    return render(request, 'administrador/index.html')

from django.shortcuts import render
from productos.models import Producto
from ventas.models import Venta

def index(request):
    productos_count = Producto.objects.count()
    ventas_total = Venta.objects.count()
    ventas_recentes = Venta.objects.all().order_by('-fecha_hora')[:5]


    return render(request, 'administrador/index.html', {
        'productos_count': productos_count,
        'ventas_total': ventas_total,
        'ventas_recentes': ventas_recentes
    })

def ventas_historial(request):
    # Aquí luego puedes implementar el historial completo
    ventas = Venta.objects.all()
    return render(request, 'administrador/ventas_historial.html', {'ventas': ventas})

def reportes(request):
    # Vista placeholder para reportes
    return render(request, 'administrador/reportes.html')
