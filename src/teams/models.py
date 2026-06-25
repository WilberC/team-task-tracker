"""Models for the teams module."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class Team(TimeStampedModel):
    name = models.CharField("nombre", max_length=140)
    area = models.ForeignKey(
        "areas.Area",
        verbose_name="area",
        on_delete=models.PROTECT,
        related_name="teams",
    )
    members = models.ManyToManyField(
        "employees.Employee",
        verbose_name="integrantes",
        related_name="teams",
        blank=True,
    )
    active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "area"],
                name="unique_team_name_per_area",
            ),
        ]
        verbose_name = "equipo"
        verbose_name_plural = "equipos"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("teams:list")

    def clean(self) -> None:
        super().clean()
        if not self.pk:
            return
        invalid_members = self.members.exclude(area=self.area)
        if invalid_members.exists():
            raise ValidationError(
                {
                    "members": (
                        "Todos los integrantes deben pertenecer al area del equipo."
                    )
                }
            )
