"""Models for the clients module."""

from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class Client(TimeStampedModel):
    full_name = models.CharField("nombre completo", max_length=160)
    phone = models.CharField("telefono", max_length=40)
    email = models.EmailField("correo", blank=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self) -> str:
        return reverse("clients:list")
