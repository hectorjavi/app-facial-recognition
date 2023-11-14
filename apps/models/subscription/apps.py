from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.models.subscription"

    def ready(self):
        __import__("apps.models.subscription.signals")
