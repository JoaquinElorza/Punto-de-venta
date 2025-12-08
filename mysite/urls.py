from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from usuarios.views import login_view

# Vista personalizada para la página principal (redirección a ventas)
def home_redirect(request):
    return redirect('ventas:punto_venta')

urlpatterns = [
    path('', login_required(home_redirect), name='home'),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    # Login (usa tu template login.html)
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Apps
    path('productos/', include('productos.urls')),
    path('ventas/', include('ventas.urls')),
    path('proveedores/', include('proveedores.urls')),

    # Página principal para vendedor
    path('', login_required(home_redirect), name='home'),

    # Página principal para admin
    path('administrador/', include(('administrador.urls', 'administrador'), namespace='administrador')),
]
