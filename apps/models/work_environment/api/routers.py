from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(r"work_environments", viewsets.WorkEnvironmentViewSet, basename="work_environments")

urlpatterns = router.get_urls()
