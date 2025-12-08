from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Proveedor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proveedor'
    )
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=150, default="")
    rfc = models.CharField(max_length=13, default="XAXX010101000")
    telefono = models.CharField(max_length=20, default="0000000000")
    correo = models.EmailField(default="sin-correo@example.com")
    direccion = models.TextField(default="Sin dirección")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.rfc})"


class Producto(models.Model):
    proveedor_nombre = models.CharField(max_length=100, verbose_name="Proveedor", default="")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default="")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default="")
    activo = models.BooleanField(default=True)
    asignado_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos_asignados"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
