import uuid
from os.path import splitext

from django.core.exceptions import ValidationError
from django.db import models

from apps.models import base_model
from apps.models.work_environment import models as work_environment
from django.core.validators import RegexValidator

NAME_MODEL_ES = "Video"
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
    return f"app_imagen/video_files/{new_filename}"


class Video(base_model.BaseModel):
    video = models.FileField(
        verbose_name="Video",
        upload_to=generate_unique_filename,
        validators=[validate_video_format],
    )
    label = models.PositiveIntegerField(
        "Etiqueta",
        blank=True,
        null=True,
        editable=False,
    )
    label_name = models.CharField(
        "Nombre de la etiqueta",
        max_length=60,
        validators=[
            RegexValidator(r'^[a-zA-Z0-9_]*$', 'Solo se permiten letras, números y guiones bajos.')
        ]
    )
    number_samples = models.PositiveSmallIntegerField(
        "Número de muestras",
        default=500
    )
    work_environment = models.ForeignKey(
        work_environment.WorkEnvironment,
        on_delete=models.RESTRICT,
        related_name="work_environment_video",
        verbose_name=work_environment.NAME_MODEL_ES,
    )

    def __str__(self):
        return str(self.label_name)

    class Meta:
        db_table = "video"
        unique_together = ("label_name", "work_environment")
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
