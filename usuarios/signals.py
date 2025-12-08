from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()  

@receiver(post_migrate)
def crear_usuarios(sender, **kwargs):
    # Crear usuario admin por defecto
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            rol="admin"
        )

    # Crear usuario vendedor por defecto
    if not User.objects.filter(username="vendedor").exists():
        User.objects.create_user(
            username="vendedor",
            email="vendedor@example.com",
            password="vendedor123",
            rol="vendedor"
        )
        
        User.objects.create_user(
    username="proveedor",
    email="proveedor@example.com",
    password="proveedor123",
    rol="proveedor"
        )

