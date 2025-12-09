from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from proveedores.models import Producto
from ventas.models import Venta


class AdminIndexViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user(
            username="admin",
            password="admin123",
            is_staff=True,
            rol="admin",
        )
        Producto.objects.create(nombre="Prod 1", precio=10, stock=5, proveedor_nombre="Prov")
        Venta.objects.create(vendedor=self.staff, total=100)

    def test_dashboard_requires_login(self):
        url = reverse("administrador:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_for_staff(self):
        self.client.login(username="admin", password="admin123")
        url = reverse("administrador:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("productos_count", response.context)
        self.assertIn("ventas_total", response.context)
