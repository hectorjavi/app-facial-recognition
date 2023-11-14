from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(r"videos", viewsets.VideoViewSet, basename="videos")

urlpatterns = router.get_urls()
