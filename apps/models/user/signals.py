from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.db import transaction
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver


from .apps import UserConfig
from .models import User


def create_default_user():
    if User.objects.filter(email="test@gmail.com").count() == 0:
        user = User(
            email="test@gmail.com",
            username="test",
            is_superuser=True,
            is_staff=True,
            password=make_password("test"),
        )
        user.full_clean()
        user.save()
        # Create permissions
        all_permissions = Permission.objects.all()
        user.user_permissions.set(all_permissions)
        user.save()


@receiver(post_migrate)
def create(sender, **kwargs):
    if isinstance(sender, UserConfig):
        create_default_user()
