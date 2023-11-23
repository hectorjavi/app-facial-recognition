from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os
import uuid
import shutil
from pathlib import Path
import zipfile

from django.conf import settings
from django.core.files import File
from apps.models.project.models import Project


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


@receiver(post_save, sender=Project)
@transaction.atomic
def post_save_project(sender, instance, created, **kwargs):
    if created:
        try:
            ia_model = instance.ia_model
            model_file_name = os.path.basename(ia_model.model_file.name)
            code_file_name = "ReconocimientoFacial.txt"
            labels_model = ia_model.labels_model

            path_template = Path(__file__).resolve().parent / "template"
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

            with open(zip_project, "rb") as zip_file:
                instance.file = File(zip_file, name=f"{uuid.uuid4()}.zip")
                instance.save()

        except Exception as ex:
            raise ex
        finally:
            pass
            if os.path.exists(base_path):
                shutil.rmtree(base_path)
        

@receiver(pre_delete, sender=Project)
@transaction.atomic
def pre_delete_project(sender, instance, **kwargs):
    instance.file.delete()
