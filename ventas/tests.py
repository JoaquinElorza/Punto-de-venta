from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from proveedores.models import Producto
from .models import Venta, DetalleVenta


class VentaModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.vendedor = User.objects.create_user(
            username="seller",
            password="pass1234",
            rol="vendedor"
        )
        self.producto = Producto.objects.create(
            nombre="Producto A",
            precio=Decimal("15.50"),
            stock=10,
            proveedor_nombre="Prov"
        )
        self.venta = Venta.objects.create(vendedor=self.vendedor)

    def test_detalle_actualiza_total_y_stock(self):
        detalle = DetalleVenta.objects.create(
            venta=self.venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=self.producto.precio,
            subtotal=Decimal("0.00"),  # se recalcula en save
        )
        self.venta.refresh_from_db()
        self.producto.refresh_from_db()

        self.assertEqual(detalle.subtotal, Decimal("31.00"))
        self.assertEqual(self.venta.total, Decimal("31.00"))
        self.assertEqual(self.producto.stock, 8)

    def test_calcular_cambio(self):
        self.venta.total = Decimal("20.00")
        self.venta.paga_con = Decimal("50.00")
        self.venta.calcular_cambio()
        self.assertEqual(self.venta.cambio, Decimal("30.00"))
