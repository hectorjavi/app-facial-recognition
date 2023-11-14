from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

VERBOSE_NAME = 'Registro "%s"'
VERBOSE_NAME_PLURAL = 'Tabla de registros "%s"'


class BaseModel(UUIDModel, TimeStampedModel):
    class Meta:
        abstract = True


class BaseModelInfo(BaseModel):
    created_by = models.UUIDField(
        default=None, null=True, blank=True, help_text="User who created the record."
    )
    modified_by = models.UUIDField(
        default=None, null=True, blank=True, help_text="User who modified the record."
    )

    class Meta:
        abstract = True
