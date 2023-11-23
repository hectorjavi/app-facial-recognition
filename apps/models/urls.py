from django.urls import include, path

urlpatterns = [
    # path("", include("apps.models.user.urls")),
    path("", include("apps.models.video.urls")),
    path("", include("apps.models.work_environment.urls")),
    path("", include("apps.models.ia_model.urls")),
    path("", include("apps.models.video_detection.urls")),
]
