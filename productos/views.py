from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm, ProductoBusquedaForm

@login_required
def lista_productos(request):
    form_busqueda = ProductoBusquedaForm(request.GET or None)
    productos = form_busqueda.filtrar() if form_busqueda.is_valid() else Producto.objects.all()
    
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'form_busqueda': form_busqueda
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/form.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/form.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:lista_productos')
    return render(request, 'productos/confirmar_eliminar.html', {'producto': producto})