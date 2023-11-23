from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.models import base_model

NAME_MODEL_ES = "Usuario"


class User(AbstractUser, base_model.BaseModelInfo):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    GENDER = [
        (MALE, "Masculino"),
        (FEMALE, "Femenino"),
        (OTHER, "Otro"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        default=OTHER,
        help_text="Género del usuario.",
        verbose_name="Género",
    )
    email = models.EmailField(
        max_length=60,
        unique=True,
        blank=False,
        null=False,
        help_text="E-mail del usuario.",
        verbose_name="E-mail",
    )

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return f"Email: {self.email}"

    class Meta:
        verbose_name = base_model.VERBOSE_NAME % NAME_MODEL_ES
        verbose_name_plural = base_model.VERBOSE_NAME_PLURAL % NAME_MODEL_ES
