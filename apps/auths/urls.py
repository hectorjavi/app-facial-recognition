from django.urls import include, path

urlpatterns = [
    path("", include("apps.auths.user.urls")),
    # path("", include("apps.auths.permission.urls")),
    # path("", include("apps.auths.group.urls")),
]
