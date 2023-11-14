from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from .. import models
# from ..permissions import HasSubscriptionCreateAudio
from . import serializers


class VideoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "put", "delete"]
    pagination_class = serializers.VideoPagination
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ["label"]
    filterset_fields = [
        "work_environment__id",
    ]
    ordering_fields = [
        "created",
        "modified",
        "label",
    ]
    ordering = ["-created"]

    def get_queryset(self, **kwargs):
        if self.request.user.is_anonymous:
            return models.Video.objects.none()
        return models.Video.objects.filter(
            work_environment__created_by=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.VideoCreateSerializer
        if self.action == "update":
            return serializers.VideoUpdateSerializer
        if self.action == "partial_update":
            return serializers.VideoPartialUpdateSerializer
        return serializers.VideoResponseSerializer
