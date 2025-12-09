from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Proveedor


class ProveedorTests(TestCase):
    def test_str_returns_nombre_y_rfc(self):
        User = get_user_model()
        user = User.objects.create_user(username="admin", password="admin123", rol="administrador")
        prov = Proveedor.objects.create(
            user=user,
            nombre="administrador X",
            rfc="XAXX010101000",
            telefono="123",
            correo="p@example.com",
            direccion="calle 1"
        )
        self.assertIn("administrador X", str(prov))
        self.assertIn("XAXX010101000", str(prov))
