from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os
import uuid
import shutil
import json
import ffmpeg

from .models import VideoDetection
from django.conf import settings
from .ia.gen_video_detection import video_detection_model
from django.core.files import File


def directory_files():
    media_root = settings.MEDIA_ROOT / "app_imagen"
    os.makedirs(media_root, exist_ok=True)
    
    media_root = media_root / "video_detection_temp"
    os.makedirs(media_root, exist_ok=True)

    media_root = media_root / str(uuid.uuid4())
    os.makedirs(media_root, exist_ok=True)

    return media_root


def convertir_mp4_a_mkv(input_file, output_file):
    input_path = input_file
    output_path = output_file
    
    ffmpeg.input(input_path).output(output_path).run()




def video_detection_create(video_detection: VideoDetection, base_path):
    # Create model
    model = video_detection.ia_model.model_file
    model_file = model.read()
    model_file_name = os.path.basename(model.name)
    new_model_file_path = base_path / model_file_name
    with open(new_model_file_path, "wb") as new_file:
        new_file.write(model_file)
    # create video
    video = video_detection.video
    video_file = video.read()
    video_file_name = os.path.basename(video.name)
    new_video_file_path = base_path / video_file_name
    with open(new_video_file_path, "wb") as new_file:
        new_file.write(video_file)
    # Using model
    video_detection_file_name = f"{uuid.uuid4()}_output.mp4"
    new_video_detection_file_path = str(base_path / video_detection_file_name)
    labels_model = json.loads(video_detection.ia_model.labels_model)
    labels_model = {valor: clave for clave, valor in labels_model.items()}
    video_detection_model(
        input_video_path=str(new_video_file_path),
        output_video_path=new_video_detection_file_path,
        modelo_path=str(new_model_file_path),
        labels_model=labels_model,
    )
    # Corregir errores video mp4 a mp4
    mkv_file_name = f"{uuid.uuid4()}_output.mp4"
    mkv_file_path = str(base_path / mkv_file_name)
    convertir_mp4_a_mkv(new_video_detection_file_path, mkv_file_path)

    with open(mkv_file_path, "rb") as video_file:
        video_detection.video_result = File(video_file, name=mkv_file_name)
        video_detection.save()


@receiver(post_save, sender=VideoDetection)
@transaction.atomic
def post_save_ia_model(sender, instance, created, **kwargs):
    if created:
        base_path = directory_files()
        try:
            video_detection_create(
                video_detection=instance,
                base_path=base_path
            )
        finally:
            try:
                shutil.rmtree(base_path)
            except Exception:  # noqa
                pass


@receiver(pre_delete, sender=VideoDetection)
@transaction.atomic
def pre_delete_video_detection(sender, instance, **kwargs):
    instance.video.delete()
    instance.video_result.delete()
