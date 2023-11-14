from django.contrib.auth.hashers import make_password
from rest_framework import pagination, serializers
from rest_framework.response import Response

from ..models import VideoDetection

class VideoDetectionPagination(pagination.PageNumberPagination):
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


class VideoDetectionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDetection
        fields = (
            "id",
            "video",
            "video_result",
            # "ia_model",
            "created",
            "modified",
        )


class VideoDetectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDetection
        fields = (
            "id",
            "video",
            "video_result",
            "ia_model",
            "created",
            "modified",
        )

    def validate_video(self, video):
        if not video:
            raise serializers.ValidationError("No se envió ningún archivo.")
        return video
    
    def validate_ia_model(self, ia_model):
        user = self.context["request"].user
        if ia_model and not (ia_model.work_environment.created_by.id == user.id):
                raise serializers.ValidationError("Modelo de IA no encontrado.")

        return ia_model
