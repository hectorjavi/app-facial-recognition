from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .. import models
from . import serializers


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    ordering_fields = [
        "created",
        "modified",
        "order",
    ]
    ordering = ["order"]

    def get_queryset(self, **kwargs):
        if self.request.user.is_anonymous:
            return models.Subscription.objects.none()
        return models.Subscription.objects.all()

    def get_serializer_class(self):
        return serializers.SubscriptionResponseSerializer
