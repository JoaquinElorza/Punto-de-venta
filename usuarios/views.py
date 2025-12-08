from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')

            # Redirecciones basadas en el rol
            if user.rol == 'admin':
                return redirect('administrador:index')
            elif user.rol == 'proveedor':
                return redirect('proveedores:dashboard')
            elif user.rol == 'vendedor':
                return redirect('ventas:punto_venta')
            else:
                return redirect('usuarios:home')

        messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, 'login.html')

    return render(request, 'login.html')


def home_view(request):
    # Vista simple para clientes o fallback
    return render(request, 'usuarios/home.html')
