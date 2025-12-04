from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="productos_index"),
    path("productos/", include("productos.urls")),
]
