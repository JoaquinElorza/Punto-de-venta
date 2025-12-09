from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):
    def test_user_rol_default_cliente(self):
        User = get_user_model()
        user = User.objects.create_user(username="u1", password="pass1234")
        self.assertEqual(user.rol, "cliente")

    def test_user_rol_custom(self):
        User = get_user_model()
        user = User.objects.create_user(username="vendedor", password="pass1234", rol="vendedor")
        self.assertEqual(user.rol, "vendedor")
