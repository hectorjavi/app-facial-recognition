from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .apps import SubscriptionConfig
from .models import Subscription


def create_default_subcription():
    subscriptions = [
        {
            "name": "Básico",
            "description": "Básico",
            "order": 1,
            "limit_audios": 5,
            "limit_images": 5,
            "limit_musics": 5,
        },
        {
            "name": "Estándar",
            "description": "Estándar",
            "order": 2,
            "limit_audios": 10,
            "limit_images": 10,
            "limit_musics": 10,
        },
        {
            "name": "Profesional",
            "description": "Profesional",
            "order": 3,
            "limit_audios": 20,
            "limit_images": 20,
            "limit_musics": 20,
        },
    ]

    for subscription_data in subscriptions:
        Subscription.objects.get_or_create(**subscription_data)


@receiver(post_migrate)
def migrate_subcription(sender, **kwargs):
    if isinstance(sender, SubscriptionConfig):
        create_default_subcription()
