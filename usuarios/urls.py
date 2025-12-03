from django.urls import path
from . import views

app_name = 'usuarios'  # Opcional: para namespacing

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    ]
