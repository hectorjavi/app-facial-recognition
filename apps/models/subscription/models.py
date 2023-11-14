from django.db import models

from apps.models import base_model

NAME_MODEL_ES = "Suscripción"


class Subscription(base_model.BaseModel):
    name = models.CharField(
        verbose_name="Nombre de la suscripción", max_length=50, unique=True
    )
    description = models.CharField(
        verbose_name="Descripción de la suscripción",
        max_length=150,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        verbose_name="Orden",
    )
    limit_audios = models.PositiveIntegerField(
        verbose_name="Límite de audios",
    )
    limit_images = models.PositiveIntegerField(
        verbose_name="Límite de imagenes",
    )
    limit_musics = models.PositiveIntegerField(
        verbose_name="Límite de músicas convertidas",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "subscription"
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
