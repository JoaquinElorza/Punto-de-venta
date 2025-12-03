
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def crear_usuarios(sender, **kwargs):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "", "admin123")

    if not User.objects.filter(username="vendedor").exists():
        User.objects.create_user("vendedor", password="vendedor123")
