from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from productos.models import Producto

class Venta(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paga_con = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completada = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"Venta #{self.id} - ${self.total}"
    
    def calcular_total(self):
        total = Decimal('0')
        for detalle in self.detalles.all():
            total += detalle.subtotal
        self.total = total
        self.save()
        return total
    
    def calcular_cambio(self):
        if self.paga_con >= self.total:
            self.cambio = self.paga_con - self.total
        else:
            self.cambio = Decimal('0')
        self.save()
        return self.cambio

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