from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

VERBOSE_NAME = 'Registro "%s"'
VERBOSE_NAME_PLURAL = 'Tabla de registros "%s"'


class BaseModel(UUIDModel, TimeStampedModel):
    class Meta:
        abstract = True

    def _mapping_values(self, values_model: dict):
        fields_model = self._meta.get_fields()
        values_model_new = {}
        for key, value in values_model.items():
            for field in fields_model:
                if field.name == key:
                    if isinstance(value, models.Model):
                        values_model_new[field.column] = value.id
                    else:
                        values_model_new[field.column] = value
                    break
        return values_model_new

    def save_values_dict(self, values_dict: dict):
        new_values = self._mapping_values(values_model=values_dict)
        self.__dict__.update(**new_values)
        self.full_clean()
        self.save()
        return self


class BaseModelInfo(BaseModel):
    created_by = models.UUIDField(
        default=None, null=True, blank=True, help_text="User who created the record."
    )
    modified_by = models.UUIDField(
        default=None, null=True, blank=True, help_text="User who modified the record."
    )

    class Meta:
        abstract = True
