from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(r"ia_models", viewsets.IAModelViewSet, basename="ia_models")

urlpatterns = router.get_urls()
