from django.contrib.auth.hashers import make_password
from rest_framework import pagination, serializers
from rest_framework.response import Response

from ..models import IAModel

class IAModelPagination(pagination.PageNumberPagination):
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


class IAModelResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAModel
        fields = (
            "id",
            "name",
            "model_file",
            "labels_model",
            # "work_environment",
            "created",
            "modified",
        )


class IAModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAModel
        fields = (
            "id",
            "name",
            "created",
            "modified",
        )


class IAModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IAModel
        fields = (
            "id",
            "name",
            "work_environment",
            "created",
            "modified",
        )

    def validate_work_environment(self, work_environment):
        user = self.context["request"].user
        if work_environment and not (work_environment.created_by.id == user.id):
                raise serializers.ValidationError("Entorno no encontrado.")

        return work_environment


class IAModelCreateProjectSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        help_text=("UUID del modelo.")
    )

    def validate_id(self, id):
        user = self.context["request"].user
        ia_models = IAModel.objects.filter(id=id, work_environment__created_by=user)
        if not ia_models.exists():
            raise serializers.ValidationError("Modelo no encontrado.")

        return id

 