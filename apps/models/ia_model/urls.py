from django.urls import include, path
from .api import viewsets


# GET, POST, PUT, PATCH, DELETE
urlpatterns = [
    path("", include("apps.models.ia_model.api.routers")),
    path(
        "ia_models/model/create_proyect/",
        viewsets.CreateModelProjectView.as_view(),
        name="create_proyect_model"
    ),
]
