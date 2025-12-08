from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from ventas.models import DetalleVenta
from proveedores.models import Proveedor

# Dashboard: proveedor ve sus productos, admin ve todos
@login_required
def dashboard_proveedor(request):
    if hasattr(request.user, "proveedor"):
        productos = Producto.objects.filter(proveedor=request.user.proveedor)
    elif request.user.is_superuser:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.none()

    return render(request, "proveedores/dashboard.html", {"productos": productos})


@login_required
def agregar_producto_proveedor(request):
    if not request.user.is_superuser and not hasattr(request.user, "proveedor"):
        messages.error(request, "No tienes permisos para agregar productos.")
        return redirect("login")

    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            messages.success(request, f"Producto '{producto.nombre}' agregado correctamente.")
            return redirect("proveedores:dashboard")
    else:
        form = ProductoForm()

    return render(request, "proveedores/form_producto_proveedor.html", {"form": form})




# Editar producto
@login_required
def editar_producto_view(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    # Validar permisos: proveedor dueño o admin
    if not request.user.is_superuser and producto.proveedor != getattr(request.user, "proveedor", None):
        messages.error(request, "No tienes permisos para editar este producto.")
        return redirect("proveedores:dashboard")

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('proveedores:dashboard')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'proveedores/form_editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    # Instancia del producto
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        # Usamos el ID del producto (entero), NO el nombre
        detalles = DetalleVenta.objects.filter(producto_id=producto.id)

        if detalles.exists():
            messages.error(
                request,
                f"No puedes eliminar el producto '{producto.nombre}' porque está vinculado a ventas."
            )
            return redirect("proveedores:dashboard")

        # Eliminar producto
        producto.delete()
        messages.success(
            request,
            f"Producto '{producto.nombre}' eliminado correctamente."
        )
        return redirect("proveedores:dashboard")

    # Si es GET, mostramos la página de confirmación
    return render(
        request,
        "proveedores/confirmar_eliminar.html",
        {"producto": producto}
    )


# Vista admin: listado completo
@staff_member_required
def listado_productos_admin(request):
    productos = Producto.objects.select_related('proveedor').order_by('-fecha_registro')
    return render(request, 'proveedores/listado_admin.html', {'productos': productos})
