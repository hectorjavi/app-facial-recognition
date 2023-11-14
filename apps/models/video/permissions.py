from rest_framework import permissions

from utils.permissions import exist_permission_model

from .models import Video


# ACL endpoint
class HasUserPermissionVideo(permissions.BasePermission):
    def has_permission(self, request, view):
        value = exist_permission_model(
            model=Video,
            method=request.method,
            user=request.user,
        )
        return value


# class HasSubscriptionCreateAudio(permissions.BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         if user is None or user.is_anonymous:
#             return False

#         if not user.subscription:
#             return False

#         if request.method == "POST":
#             audio_count = Audio.objects.filter(created_by=user).count()
#             if audio_count >= user.subscription.limit_audios:
#                 return False
#         return True
