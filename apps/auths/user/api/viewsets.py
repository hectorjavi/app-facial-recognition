from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models.user.api.serializers import UserRegisterSerializer as UsRSLR
from apps.models.user.api.serializers import UserSerializer as UsSLR
from apps.models.user.models import User

from . import serializers


class LoginView(TokenObtainPairView):
    serializers_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializers_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = UsSLR(login_serializer.user, context={"request": request}).data
        response = login_serializer.validated_data
        response["user"] = user
        return Response(
            response,
            status=status.HTTP_200_OK,
        )


class RegisterViewSet(viewsets.ModelViewSet):
    # permission_classes = [HasAPIKey]
    serializer_class = UsRSLR
    http_method_names = ["post"]
    queryset = User.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        del data["password"]
        headers = self.get_success_headers(data)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UsSLR()})
    def get(self, request):
        serializers_data = UsSLR(request.user, context={"request": request})
        return Response(serializers_data.data)

    # Actualizar usuario
    @swagger_auto_schema(
        responses={200: UsSLR()},
        request_body=serializers.UserMeUpdateSerializer(),
    )
    def patch(self, request):
        user = User.objects.get(id=request.user.id)
        serializer_data = serializers.UserMeUpdateSerializer(user, request.data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            serializers_data_new = UsSLR(
                User.objects.get(id=request.user.id), context={"request": request}
            )
            return Response(serializers_data_new.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer_data.errors)


class UserMePassView(APIView):
    permission_classes = [HasAPIKey, IsAuthenticated]

    # Actualizar passwords
    @swagger_auto_schema(
        responses={200: {}}, request_body=serializers.UserMeUpdatePssSerializer()
    )
    def post(self, request):
        serializer_data = serializers.UserMeUpdatePssSerializer(data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            user = authenticate(
                email=request.user.email,
                username=request.user.username,
                password=serializer_data.data["current_password"],
            )
            if user:
                user.password = make_password(serializer_data.data["new_password"])
                user.save()
                return Response()
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"current_password": ["Contraseña incorrecta."]},
                )
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer_data.errors)
