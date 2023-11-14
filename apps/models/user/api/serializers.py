from django.contrib.auth.hashers import make_password
from rest_framework import pagination, serializers
from rest_framework.response import Response

from apps.auths.group.api.serializers import GroupSerializer
from apps.auths.permission.api.serializers import PermissionSerializer
from apps.models.user.models import User

from ...subscription.api.serializers import SubscriptionResponseSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "page_number": self.page.number,
                "page_size": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)
    # user_permissions = PermissionSerializer(many=True)
    gender = serializers.CharField(source="get_gender_display")
    subscription = SubscriptionResponseSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_active",
            "created",
            "modified",
            "gender",
            "email",
            "subscription",
            # "groups",
            # "user_permissions",
        )


class UserSimpleResponseSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="get_gender_display")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "created",
            "modified",
            "gender",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )

    def validate_password(self, password):
        if password is not None:
            password = make_password(password)

        return password


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "gender",
            "password",
            "created",
            "modified",
        )

    def validate_password(self, password):
        if password is not None:
            password = make_password(password)

        return password
