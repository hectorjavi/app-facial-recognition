from rest_framework import permissions

from utils.permissions import exist_permission_model

from .models import User


# ACL endpoint
class HasUserPermissionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        value = exist_permission_model(
            model=User,
            method=request.method,
            user=request.user,
        )
        return value
