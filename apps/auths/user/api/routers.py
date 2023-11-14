from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(r"register", viewsets.RegisterViewSet, basename="register")

urlpatterns = router.get_urls()
