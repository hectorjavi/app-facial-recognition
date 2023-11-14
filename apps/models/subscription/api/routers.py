from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()


router.register(
    r"subscriptions", viewsets.SubscriptionViewSet, basename="subscriptions"
)

urlpatterns = router.get_urls()
