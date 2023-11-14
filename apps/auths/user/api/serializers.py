from rest_framework import serializers

from apps.models.user.models import User


class UserMeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "gender",
            "email",
        )


class UserMeUpdatePssSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        help_text=("Contraseña actual del usuario.")
    )
    new_password = serializers.CharField(help_text=("Nueva contraseña del usuario."))

    def validate(self, data):
        if data["current_password"] == data["new_password"]:
            raise serializers.ValidationError(
                {"new_password": "Ingrese una contraseña diferente al anterior."}
            )
        return data
