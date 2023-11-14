from django.apps import AppConfig


class VideoDetectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.models.video_detection"

    def ready(self):
        __import__("apps.models.video_detection.signals")