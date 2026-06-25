"""Models for the vehicles module."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class Vehicle(TimeStampedModel):
    client = models.ForeignKey(
        "clients.Client",
        verbose_name="cliente",
        on_delete=models.PROTECT,
        related_name="vehicles",
    )
    plate = models.CharField("placa", max_length=20)
    make = models.CharField("marca", max_length=80)
    model = models.CharField("modelo", max_length=80)
    year = models.PositiveSmallIntegerField(
        "anio",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
        ],
    )

    class Meta:
        ordering = ["plate"]
        constraints = [
            models.UniqueConstraint(
                fields=["plate"],
                name="unique_vehicle_plate",
            ),
        ]
        verbose_name = "vehiculo"
        verbose_name_plural = "vehiculos"

    def __str__(self) -> str:
        return f"{self.plate} - {self.make} {self.model}"

    def get_absolute_url(self) -> str:
        return reverse("vehicles:list")
