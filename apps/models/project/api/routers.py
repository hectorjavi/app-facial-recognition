from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(r"projects", viewsets.ProjectViewSet, basename="projects")

urlpatterns = router.get_urls()
