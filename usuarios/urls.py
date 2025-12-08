from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, home_view

app_name = 'usuarios'

urlpatterns = [
    # Login con tu vista personalizada
    path('login/', login_view, name='login'),

    # Logout con la vista de Django
    path('logout/', auth_views.LogoutView.as_view(next_page='usuarios:login'), name='logout'),

    # Home para clientes o fallback
    path('home/', home_view, name='home'),
]
