from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from pathlib import Path
import zipfile
import shutil

import uuid
import os
from .. import models
from . import serializers
import base64
from django.http import HttpResponse


class IAModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "put", "delete"]
    pagination_class = serializers.IAModelPagination
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ["name"]
    filterset_fields = [
        "work_environment__id",
    ]
    ordering_fields = [
        "created",
        "modified",
        "name",
    ]

    def get_queryset(self, **kwargs):
        if self.request.user.is_anonymous:
            return models.IAModel.objects.none()
        return models.IAModel.objects.filter(
            work_environment__created_by=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.IAModelCreateSerializer
        if self.action == "update" or self.action == "partial_update":
            return serializers.IAModelUpdateSerializer
        return serializers.IAModelResponseSerializer



def directory_files():
    media_root = settings.MEDIA_ROOT / "app_imagen"
    os.makedirs(media_root, exist_ok=True)
    
    media_root = media_root / "ia_project_temp"
    os.makedirs(media_root, exist_ok=True)

    media_root = media_root / str(uuid.uuid4())
    os.makedirs(media_root, exist_ok=True)

    return media_root


def comprimir_archivos(archivos_a_comprimir, nombre_archivo_salida, formato='zip'):
    try:
        # Obtiene el directorio base de los archivos
        directorio_base = os.path.dirname(archivos_a_comprimir[0])  # Suponiendo que todos los archivos están en el mismo directorio
        
        with zipfile.ZipFile(nombre_archivo_salida, 'w' if formato == 'zip' else 'x', compression=zipfile.ZIP_DEFLATED) as archivo_zip:
            for ruta_archivo in archivos_a_comprimir:
                # Agrega el archivo al archivo comprimido
                archivo_zip.write(ruta_archivo, os.path.relpath(ruta_archivo, directorio_base))
    except Exception as e:
        raise e


def file_to_base64(file_path):
        with open(file_path, "rb") as file:
            binary_content = file.read()
            base64_content = base64.b64encode(binary_content)
            base64_str = base64_content.decode("utf-8")
            return base64_str

class CreateModelProjectView(APIView):
    permission_classes = [IsAuthenticated]

    # Actualizar usuario
    @swagger_auto_schema(
        # responses={200: UsSLR()},
        request_body=serializers.IAModelCreateProjectSerializer(),
    )
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = serializers.IAModelCreateProjectSerializer(
                data=data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            ia_model = models.IAModel.objects.get(id=data["id"])
            model_file_name = os.path.basename(ia_model.model_file.name)
            code_file_name = "ReconocimientoFacial.txt"
            labels_model = ia_model.labels_model

            path_template = Path(__file__).resolve().parent.parent / "template"
            code_file_path = path_template / code_file_name
            with open(code_file_path, 'r') as archivo:
                code_python = archivo.read()

            requeriments_file_path = path_template / "requirements.txt"
            with open(requeriments_file_path, 'r') as requirements_file:
                requirements = requirements_file.read()

            code_python = code_python.replace("'aqui_cambiar_labels'", labels_model)
            code_python = code_python.replace("'modeloLBPHFace.xml'", f"\"{model_file_name}\"")

            base_path = directory_files()
            ia_model_file = ia_model.model_file.read()
            model_file_path = base_path / model_file_name
            with open(model_file_path, "wb") as file:
                file.write(ia_model_file)
            
            code_file_path = base_path / "ReconocimientoFacial.py"
            # Abre el archivo en modo escritura ('w')
            with open(code_file_path, 'w') as file:
                file.write(code_python)
            
            requirements_file_path = base_path / "requirements.txt"
            with open(requirements_file_path, 'w') as file:
                file.write(requirements)

            files_for_zip = [
                str(model_file_path),
                str(code_file_path),
                str(requirements_file_path),
            ]
            zip_project = str(base_path / 'comprimido.zip')
            comprimir_archivos(files_for_zip, zip_project)

            base64 = file_to_base64(str(zip_project))
            return Response(
                status=200,
                data={"base64_file": base64}
            )
            # with open(zip_project, 'rb') as file:
            #     response = HttpResponse(file.read(), content_type='application/zip')
            #     response['Content-Disposition'] = 'attachment; filename=temp_file.zip'  # Nombre del archivo de descarga
            #     return response
        except Exception as ex:
            return Response(
                status=500,
                data={"detail": str(ex)}
            )
        finally:
            if os.path.exists(base_path):
                shutil.rmtree(base_path)