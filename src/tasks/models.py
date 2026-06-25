"""Models for the tasks module."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from src.common.models import TimeStampedModel


class TaskPriority(models.TextChoices):
    LOW = "low", "Baja"
    MEDIUM = "medium", "Media"
    HIGH = "high", "Alta"
    CRITICAL = "critical", "Critica"


class TaskStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    IN_PROGRESS = "in_progress", "En progreso"
    COMPLETED = "completed", "Completada"
    OVERDUE = "overdue", "Vencida"
    CANCELLED = "cancelled", "Cancelada"


class Task(TimeStampedModel):
    title = models.CharField("titulo", max_length=180)
    description = models.TextField("descripcion", blank=True)
    job_order = models.ForeignKey(
        "workshop.JobOrder",
        verbose_name="orden de trabajo",
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True,
        null=True,
    )
    parent_task = models.ForeignKey(
        "self",
        verbose_name="tarea principal",
        on_delete=models.CASCADE,
        related_name="subtasks",
        blank=True,
        null=True,
    )
    area = models.ForeignKey(
        "areas.Area",
        verbose_name="area",
        on_delete=models.PROTECT,
        related_name="tasks",
    )
    assigned_employee = models.ForeignKey(
        "employees.Employee",
        verbose_name="empleado responsable",
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
        blank=True,
        null=True,
    )
    assigned_team = models.ForeignKey(
        "teams.Team",
        verbose_name="equipo responsable",
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
        blank=True,
        null=True,
    )
    priority = models.CharField(
        "prioridad",
        max_length=20,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM,
    )
    status = models.CharField(
        "estado",
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING,
    )
    start_date = models.DateField("fecha de inicio", blank=True, null=True)
    due_date = models.DateField("fecha limite")
    completion_date = models.DateField("fecha de finalizacion", blank=True, null=True)

    class Meta:
        ordering = ["due_date", "priority", "title"]
        verbose_name = "tarea"
        verbose_name_plural = "tareas"

    def __str__(self) -> str:
        return self.title

    @property
    def is_subtask(self) -> bool:
        return self.parent_task_id is not None

    @property
    def is_top_level(self) -> bool:
        return self.parent_task_id is None

    def clean(self) -> None:
        super().clean()
        errors = {}

        if self.parent_task_id:
            if self.job_order_id:
                errors["job_order"] = (
                    "Una subtarea hereda la orden de trabajo de su tarea principal."
                )
            if self.parent_task and self.parent_task.parent_task_id:
                errors["parent_task"] = "Una subtarea no puede tener subtareas."
            if not self.area_id and self.parent_task:
                self.area = self.parent_task.area
        elif not self.job_order_id:
            errors["job_order"] = (
                "Una tarea principal debe pertenecer a una orden de trabajo."
            )

        if self.assigned_employee_id and self.assigned_team_id:
            errors["assigned_team"] = (
                "Asigne la tarea a un empleado o a un equipo, no a ambos."
            )
        elif not self.assigned_employee_id and not self.assigned_team_id:
            errors["assigned_employee"] = (
                "Seleccione un empleado o un equipo responsable."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.parent_task_id and not self.area_id:
            self.area = self.parent_task.area
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("tasks:detail", args=[self.pk])
