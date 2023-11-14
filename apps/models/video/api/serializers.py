import magic
from drf_extra_fields.fields import Base64FileField
from rest_framework import pagination, serializers
from rest_framework.response import Response

from ..models import Video


class VideoPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 300

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


class VideoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "video",
            "label_name",
            "created",
            "modified",
        )


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "video",
            "label_name",
            "work_environment",
            "number_samples",
            "created",
            "modified",
        )

    def validate_video(self, video):
        if not video:
            raise serializers.ValidationError("No se envió ningún archivo.")
        return video
    
    def validate_work_environment(self, work_environment):
        user = self.context["request"].user
        if work_environment and not (work_environment.created_by.id == user.id):
                raise serializers.ValidationError("Entorno no encontrado.")

        return work_environment


class VideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "label_name",
            "created",
            "modified",
        )


class VideoPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "id",
            "label_name",
            "created",
            "modified",
        )