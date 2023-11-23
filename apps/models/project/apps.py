from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.models.project'

    def ready(self):
        __import__("apps.models.project.signals")
