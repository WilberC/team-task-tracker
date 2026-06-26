"""Models for the employees module."""

from django.conf import settings
from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class Employee(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="usuario",
        on_delete=models.SET_NULL,
        related_name="employee_profile",
        blank=True,
        null=True,
    )
    full_name = models.CharField("nombre completo", max_length=160)
    email = models.EmailField("correo", blank=True)
    area = models.ForeignKey(
        "areas.Area",
        verbose_name="area",
        on_delete=models.PROTECT,
        related_name="employees",
    )
    position = models.CharField("cargo", max_length=120)
    active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "empleado"
        verbose_name_plural = "empleados"

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self) -> str:
        return reverse("employees:list")
