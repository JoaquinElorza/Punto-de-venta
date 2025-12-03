from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    """
    Vista para manejar el login de usuarios.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Por favor, ingrese tanto el usuario como la contraseña.')
            # RENDERIZA EL TEMPLATE EN LA RUTA CORRECTA
            return render(request, 'usuarios/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            # RENDERIZA EL TEMPLATE EN LA RUTA CORRECTA
            return render(request, 'usuarios/login.html')
    
    # RENDERIZA EL TEMPLATE EN LA RUTA CORRECTA
    return render(request, 'usuarios/login.html')

@login_required
def home_view(request):
    """
    Vista de la página principal protegida por autenticación.
    """
    # RENDERIZA EL TEMPLATE EN LA RUTA CORRECTA
    return render(request, 'usuarios/home.html', {'user': request.user})

@login_required
def logout_view(request):
    """
    Vista para cerrar sesión.
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')