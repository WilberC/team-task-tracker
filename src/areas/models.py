"""Models for the areas module."""

from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class Area(TimeStampedModel):
    name = models.CharField("nombre", max_length=120, unique=True)
    description = models.TextField("descripcion", blank=True)
    active = models.BooleanField("activa", default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "area"
        verbose_name_plural = "areas"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("areas:list")
