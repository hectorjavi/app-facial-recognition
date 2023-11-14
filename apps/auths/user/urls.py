from django.urls import include, path
from rest_framework_simplejwt.views import TokenBlacklistView as TokenBlacklist
from rest_framework_simplejwt.views import TokenRefreshView as TokenRefresh
from rest_framework_simplejwt.views import TokenVerifyView as TokenVerify

from apps.auths.user.api import viewsets

urlpatterns = [
    path("auth/token/verify/", TokenVerify.as_view(), name="token_verify"),
    # path("auth/token/refresh/", TokenRefresh.as_view(), name="token_refresh"),
    # path("auth/token/blacklist/", TokenBlacklist.as_view(), name="token_blacklist"),
    path("auth/token/", viewsets.LoginView.as_view(), name="token_refresh_v2"),
    path("auth/me/", viewsets.UserMeView.as_view(), name="user_me"),
    path(
        "auth/me/reset_password/",
        viewsets.UserMePassView.as_view(),
        name="user_me_reset_password",
    ),
    path("auth/", include("apps.auths.user.api.routers")),
]
