from django.db import models

from apps.models import base_model
from apps.models.work_environment import models as work_environment

NAME_MODEL_ES = "IAModel"


class IAModel(base_model.BaseModel):
    name = models.CharField(
        verbose_name="Nombre del modelo de inteligencia artificial",
        max_length=50,
    )
    model_file = models.FileField(
        verbose_name="model",
        upload_to="app_imagen/model_files/",
        blank=True,
        null=True,
        editable=False
    )
    labels_model = models.JSONField(
        verbose_name="Etiquetas del modelo",
        blank=True,
        null=True,
        editable=False,
    )
    work_environment = models.ForeignKey(
        work_environment.WorkEnvironment,
        on_delete=models.RESTRICT,
        related_name="work_environment_ia_model",
        verbose_name=work_environment.NAME_MODEL_ES,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "ia_model"
        unique_together = ("name", "work_environment")
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
