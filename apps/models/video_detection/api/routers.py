from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(r"video_detections", viewsets.VideoDetectionViewSet, basename="video_detections")

urlpatterns = router.get_urls()
