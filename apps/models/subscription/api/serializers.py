from rest_framework import serializers

from ..models import Subscription


class SubscriptionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "name",
            "description",
            "limit_audios",
            "limit_images",
            "limit_musics",
        )


class SubscriptionSimpleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            "name",
            "description",
            "limit_audios",
            "limit_images",
            "limit_musics",
        )
