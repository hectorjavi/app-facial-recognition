from django.contrib.auth.hashers import make_password
from rest_framework import pagination, serializers
from rest_framework.response import Response

from ..models import WorkEnvironment

class WorkEnvironmentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "number": self.page.number,
                "page_size": self.get_page_size(self.request),
                "next_link": self.get_next_link(),
                "previous_link": self.get_previous_link(),
                "results": data,
            }
        )


class WorkEnvironmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEnvironment
        fields = (
            "id",
            "name",
            "created",
            "modified",
        )


class WorkEnvironmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEnvironment
        fields = (
            "id",
            "name",
            "created",
            "modified",
        )


class WorkEnvironmentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEnvironment
        fields = (
            "id",
            "name",
            "created",
            "modified",
        )


class WorkEnvironmentRegisterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkEnvironment
        fields = (
            "id",
            "name",
            "created_by",
            "created",
            "modified",
        )
