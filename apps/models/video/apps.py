from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.models.video"

    def ready(self):
        __import__("apps.models.video.signals")
