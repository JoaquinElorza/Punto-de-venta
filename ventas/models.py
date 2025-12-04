from django.db import models
from productos.models import Producto
from django.core.validators import MinValueValidator

class Venta(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paga_con = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completada = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_hora']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
    
    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"
    
    def calcular_total(self):
        """Calcula el total de la venta sumando los detalles"""
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save()
        return total
    
    def calcular_cambio(self):
        """Calcula el cambio a devolver"""
        if self.paga_con >= self.total:
            self.cambio = self.paga_con - self.total
        else:
            self.cambio = 0
        self.save()
        return self.cambio

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Venta'
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    def calcular_subtotal(self):
        """Calcula el subtotal del detalle"""
        self.subtotal = self.cantidad * self.precio_unitario
        self.save()
        return self.subtotal
    
    def save(self, *args, **kwargs):
        # Si no se especifica el precio unitario, usar el precio del producto
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio_venta
        
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        
        super().save(*args, **kwargs)
        
        # Actualizar el stock del producto
        self.producto.stock -= self.cantidad
        self.producto.save()
        
        # Recalcular total de la venta
        self.venta.calcular_total()