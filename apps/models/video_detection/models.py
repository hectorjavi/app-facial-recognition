import uuid
from os.path import splitext

from django.core.exceptions import ValidationError
from django.db import models

from apps.models import base_model
from apps.models.ia_model import models as ia_model

NAME_MODEL_ES = "Detección de videos"
# extensions_music = [".mp4",]
extensions_video = [".mp4", ".webm", ".mkv", ".avi"]


def validate_video_format(value):
    ext = value.name
    if not value:
        raise ValidationError(f'Video es requerido.')
    _, ext = splitext(value.name)
    if ext not in extensions_video:
        raise ValidationError(f'Formato incorrecto {ext}. Use: [{", ".join(extensions_video)}].')


def generate_unique_filename(instance, filename):
    unique_filename = str(uuid.uuid4())
    ext = filename.split(".")[-1]
    new_filename = f"{unique_filename}.{ext}"
    return f"app_imagen/video_detection_files/{new_filename}"


class VideoDetection(base_model.BaseModel):
    video = models.FileField(
        verbose_name="Video",
        upload_to=generate_unique_filename,
        validators=[validate_video_format],
    )
    video_result = models.FileField(
        verbose_name="Resultado del Video",
        upload_to=generate_unique_filename,
        blank=True,
        null=True,
        editable=False
    )
    ia_model = models.ForeignKey(
        ia_model.IAModel,
        on_delete=models.RESTRICT,
        related_name="ia_model_video_detection",
        verbose_name=ia_model.NAME_MODEL_ES,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "video_detection"
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
