from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .. import models
from . import serializers


class VideoDetectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "delete"]
    pagination_class = serializers.VideoDetectionPagination
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    # search_fields = ["name"]
    filterset_fields = [
        "ia_model__work_environment__id",
        "ia_model__id"
    ]
    ordering_fields = [
        "created",
        "modified",
    ]

    def get_queryset(self, **kwargs):
        if self.request.user.is_anonymous:
            return models.VideoDetection.objects.none()
        return models.VideoDetection.objects.filter(
            ia_model__work_environment__created_by=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.VideoDetectionCreateSerializer
        return serializers.VideoDetectionResponseSerializer
