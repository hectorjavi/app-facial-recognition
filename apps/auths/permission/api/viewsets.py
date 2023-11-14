from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from . import serializers


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey, IsAuthenticated]
    serializer_class = serializers.PermissionSerializer
    http_method_names = ["get"]
    queryset = serializers.Permission.objects.exclude(
        Q(codename__icontains="Logentry")
        | Q(codename__icontains="session")
        | Q(codename__icontains="contenttype")
        | Q(codename__icontains="Blacklistedtoken")
        | Q(codename__icontains="Outstandingtoken")
    )
