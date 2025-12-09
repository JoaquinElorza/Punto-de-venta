from decimal import Decimal
from django.test import TestCase
from proveedores.models import Producto


class ProductoTests(TestCase):
    def test_str_and_defaults(self):
        p = Producto.objects.create(
            nombre="Prod Test",
            descripcion="desc",
            precio=Decimal("9.99"),
            stock=5,
            proveedor_nombre="Prov",
        )
        self.assertEqual(str(p), "Prod Test")
        self.assertTrue(p.activo)
