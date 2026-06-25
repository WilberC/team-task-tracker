"""Models for the sales module."""

from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class ServiceOrderStatus(models.TextChoices):
    OPEN = "open", "Abierta"
    APPROVED = "approved", "Aprobada"
    CLOSED = "closed", "Cerrada"


class ServiceOrder(TimeStampedModel):
    client = models.ForeignKey(
        "clients.Client",
        verbose_name="cliente",
        on_delete=models.PROTECT,
        related_name="service_orders",
    )
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        verbose_name="vehiculo",
        on_delete=models.PROTECT,
        related_name="service_orders",
    )
    advisor = models.ForeignKey(
        "employees.Employee",
        verbose_name="asesor",
        on_delete=models.PROTECT,
        related_name="service_orders",
        blank=True,
        null=True,
    )
    description = models.TextField("descripcion")
    status = models.CharField(
        "estado",
        max_length=20,
        choices=ServiceOrderStatus.choices,
        default=ServiceOrderStatus.OPEN,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "orden de servicio"
        verbose_name_plural = "ordenes de servicio"

    def __str__(self) -> str:
        return f"OS-{self.pk or 'nueva'} - {self.client}"

    def get_absolute_url(self) -> str:
        return reverse("sales:list")
