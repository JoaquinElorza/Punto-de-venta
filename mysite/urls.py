"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from usuarios.views import redirect_after_login

# Vista personalizada para la página principal (redirección a ventas)
def home_redirect(request):
    return redirect('ventas:punto_venta')

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

# Vista personalizada para la página principal (redirección a ventas)
def home_redirect(request):
    return redirect('ventas:punto_venta')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Login
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True,
        next_page='redirect_after_login'    
    ), name='login'),

    # Logout (usando LogoutView de Django)
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Apps
    path('productos/', include('productos.urls')),
    path('ventas/', include('ventas.urls')),

    path('redirect/', redirect_after_login, name='redirect_after_login'),

    # Página principal para vendedor
    path('', login_required(home_redirect), name='home'),

    # Página principal para admin
    path('administrador/', include(('administrador.urls', 'administrador'), namespace='administrador')),


    

]
