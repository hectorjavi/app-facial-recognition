from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Backend",
        default_version="V1",
        description="Backend",
        contact=openapi.Contact(email="hectorjavier@upeu.edu.pe"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
