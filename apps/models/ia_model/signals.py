from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os
import uuid
import shutil
import json

from .models import IAModel
from ..video.models import Video
from .ia.gen_data import data_generation
from .ia.gen_model import gen_model
from django.conf import settings
from django.core.files import File


def directory_files():
    media_root = settings.MEDIA_ROOT / "app_imagen"
    if not os.path.exists(media_root):
        os.makedirs(media_root)

    media_root = media_root / "dataset_temp"
    if not os.path.exists(media_root):
        os.makedirs(media_root)
    
    media_root = media_root / str(uuid.uuid4())
    if not os.path.exists(media_root):
        os.makedirs(media_root)
    
    return media_root


def gen_data_by_person(instance: IAModel, base_path):
    videos_env = Video.objects.filter(work_environment=instance.work_environment)
    label_video = {}
    for video in videos_env:
        label_video[video.label_name] = video.label
        label_name = video.label_name
        number_samples = video.number_samples
        contenido_video = video.video.read()
        _, extension = os.path.splitext(video.video.name)
        video_path = base_path / f"{label_name}{extension}"
        with open(video_path, "wb") as archivo_destino:
            archivo_destino.write(contenido_video)

        data_generation(
            data_path=base_path,
            max_images=number_samples,
            person_name=label_name,
            video_path=video_path,
        )

    model_name = f'{uuid.uuid4()}_modeloLBPHFace.xml'
    model_path = base_path / model_name
    gen_model(
        data_path=base_path,
        model_path=model_path,
        dict_label_name_dir=label_video
    )
    with open(model_path, "rb") as model_file:
        instance.model_file = File(model_file, name=model_name)
        instance.labels_model = json.dumps(label_video)
        instance.save()


@receiver(post_save, sender=IAModel)
@transaction.atomic
def post_save_ia_model(sender, instance, created, **kwargs):
    if created:
        base_path = directory_files()
        try:
            gen_data_by_person(instance=instance, base_path=base_path)
        finally:
            if os.path.exists(base_path):
                shutil.rmtree(base_path)


@receiver(pre_delete, sender=IAModel)
@transaction.atomic
def pre_delete_ia_model(sender, instance, **kwargs):
    instance.model_file.delete()
