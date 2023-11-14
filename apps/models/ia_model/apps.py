from django.apps import AppConfig


class IaModelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.models.ia_model"

    def ready(self):
        __import__("apps.models.ia_model.signals")
