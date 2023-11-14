from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .. import models
from . import serializers


class WorkEnvironmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "put", "delete"]
    pagination_class = serializers.WorkEnvironmentPagination
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ["name"]
    ordering_fields = [
        "created",
        "modified",
        "name",
    ]

    def get_queryset(self, **kwargs):
        if self.request.user.is_anonymous:
            return models.WorkEnvironment.objects.none()
        return models.WorkEnvironment.objects.filter(
            created_by=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.WorkEnvironmentRegisterSerializer
        if self.action == "update" or self.action == "partial_update":
            return serializers.WorkEnvironmentUpdateSerializer
        return serializers.WorkEnvironmentResponseSerializer
    
    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        serializer = serializers.WorkEnvironmentRegisterInfoSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
