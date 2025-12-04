from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages


def redirect_after_login(request):
    user = request.user
    # recarga info del usuario
    user.refresh_from_db()

    if user.is_staff:  # admin
        return redirect('administrador:index')
    else:
        return redirect('ventas:punto_venta')



@csrf_protect
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Por favor, ingrese tanto el usuario como la contraseña.')
            return render(request, 'usuarios/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')

            # Redirecciones según tipo de usuario
            if user.is_superuser:
                return redirect('administrador:index')   # ADMIN
            elif user.is_staff:
                return redirect('ventas:punto_venta')    # VENDEDOR
            else:
                return redirect('usuarios:home')         # USUARIO NORMAL

        messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, 'usuarios/login.html')

    return render(request, 'usuarios/login.html')
