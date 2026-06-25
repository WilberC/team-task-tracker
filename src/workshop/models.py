"""Models for the workshop module."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from src.common.models import TimeStampedModel


class JobOrderStatus(models.TextChoices):
    OPEN = "open", "Abierta"
    IN_PROGRESS = "in_progress", "En progreso"
    DONE = "done", "Terminada"
    DELIVERED = "delivered", "Entregada"


class JobOrder(TimeStampedModel):
    service_order = models.OneToOneField(
        "sales.ServiceOrder",
        verbose_name="orden de servicio",
        on_delete=models.PROTECT,
        related_name="job_order",
    )
    vehicle = models.ForeignKey(
        "vehicles.Vehicle",
        verbose_name="vehiculo",
        on_delete=models.PROTECT,
        related_name="job_orders",
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=JobOrderStatus.choices,
        default=JobOrderStatus.OPEN,
    )
    interned_at = models.DateTimeField("fecha de internamiento", default=timezone.now)
    closed_at = models.DateTimeField("fecha de cierre", blank=True, null=True)

    class Meta:
        ordering = ["-interned_at"]
        verbose_name = "orden de trabajo"
        verbose_name_plural = "ordenes de trabajo"

    def __str__(self) -> str:
        return f"OT-{self.pk or 'nueva'} - {self.vehicle.plate}"

    def clean(self) -> None:
        super().clean()
        if (
            self.service_order_id
            and self.vehicle_id
            and self.service_order.vehicle_id != self.vehicle_id
        ):
            raise ValidationError(
                {"vehicle": ("El vehiculo debe coincidir con la orden de servicio.")}
            )

    def get_absolute_url(self) -> str:
        return reverse("workshop:detail", args=[self.pk])
