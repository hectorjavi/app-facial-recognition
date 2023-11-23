from django.db import models
import uuid

from apps.models import base_model
from apps.models.ia_model import models as ia_model


NAME_MODEL_ES = "Proyecto"


def generate_unique_filename(instance, filename):
    unique_filename = str(uuid.uuid4())
    ext = filename.split(".")[-1]
    new_filename = f"{unique_filename}.{ext}"
    return f"app_imagen/project/{new_filename}"


class Project(base_model.BaseModel):
    file = models.FileField(
        verbose_name="Archivo",
        upload_to=generate_unique_filename,
        editable=False
    )

    ia_model = models.ForeignKey(
        ia_model.IAModel,
        on_delete=models.RESTRICT,
        related_name="ia_model_project",
        verbose_name=ia_model.NAME_MODEL_ES,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "project"
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
