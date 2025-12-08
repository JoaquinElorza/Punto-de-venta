from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from proveedores.models import Producto
from django.conf import settings
from django.db.models import Sum
from decimal import Decimal

class Venta(models.Model):
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas"
    )
    fecha_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paga_con = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Venta #{self.id} - {self.total}"

    def calcular_total(self):
        agg = self.detalles.aggregate(suma=Sum('subtotal'))
        self.total = agg['suma'] or Decimal('0.00')

    def calcular_cambio(self):
        if self.paga_con is not None:
            self.cambio = self.paga_con - self.total

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    def save(self, *args, **kwargs):
        # Si no se especifica el precio, usar el precio del producto
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio
        
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        
        super().save(*args, **kwargs)
        
        # Actualizar stock del producto
        self.producto.stock -= self.cantidad
        self.producto.save()
        
        # Actualizar total de la venta
        self.venta.calcular_total()