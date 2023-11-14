from django.db import models

from apps.models import base_model
from apps.models.user import models as user

NAME_MODEL_ES = "Entorno de Desarrollo"


class WorkEnvironment(base_model.BaseModel):
    name = models.CharField(
        verbose_name="Nombre del entorno de desarrollo", max_length=50, unique=True
    )

    created_by = models.ForeignKey(
        user.User,
        on_delete=models.RESTRICT,
        related_name="created_by_work_environment",
        verbose_name=user.NAME_MODEL_ES,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "work_environment"
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
