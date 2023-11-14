from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework_api_key.permissions import HasAPIKey

from apps.models.user.permissions import HasUserPermissionUser

from .. import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey, HasUserPermissionUser]
    serializer_class = serializers.UserSerializer
    http_method_names = ["post", "get", "patch", "put", "delete"]
    pagination_class = serializers.CustomPagination
    queryset = models.User.objects.filter().order_by("email")
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ["username", "email", "dni"]
    filterset_fields = ["gender"]
    ordering_fields = [
        "created",
        "modified",
    ]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserRegisterSerializer
        if self.action == "update" or self.action == "partial_update":
            return serializers.UserUpdateSerializer
        return self.serializer_class
