"""Read/query helpers for the workshop module."""

from dataclasses import dataclass
from uuid import UUID

from django.db.models import QuerySet

from src.tasks.models import TaskStatus
from src.workshop.models import JobOrder, JobOrderStatus


@dataclass(frozen=True)
class ClientSafeJob:
    title: str
    status_label: str
    status_kind: str


@dataclass(frozen=True)
class ClientSafeProgress:
    total: int
    done: int
    percent: int
    summary: str


@dataclass(frozen=True)
class ClientSafeJobOrderStatus:
    vehicle_plate: str
    vehicle_make: str
    vehicle_model: str
    vehicle_year: int
    overall_status_label: str
    overall_status_kind: str
    progress: ClientSafeProgress
    jobs: tuple[ClientSafeJob, ...]


def job_orders_list() -> QuerySet[JobOrder]:
    return JobOrder.objects.select_related(
        "service_order__client",
        "vehicle",
    ).order_by("-interned_at")


def open_job_orders() -> QuerySet[JobOrder]:
    return job_orders_list().exclude(status=JobOrderStatus.DELIVERED)


def job_order_with_tasks(pk: int | str) -> JobOrder:
    return job_orders_list().prefetch_related("tasks__subtasks").get(pk=pk)


def client_safe_job_order_status(token: UUID | str) -> ClientSafeJobOrderStatus:
    job_order = (
        JobOrder.objects.select_related("vehicle")
        .prefetch_related("tasks")
        .get(client_status_token=token)
    )
    tasks = [task for task in job_order.tasks.all() if task.parent_task_id is None]
    jobs = tuple(
        ClientSafeJob(
            title=task.title,
            status_label=_friendly_task_status(task.status),
            status_kind=task.status,
        )
        for task in tasks
    )
    done = sum(
        1
        for task in tasks
        if task.status in {TaskStatus.COMPLETED, TaskStatus.CANCELLED}
    )
    total = len(tasks)
    progress = ClientSafeProgress(
        total=total,
        done=done,
        percent=round((done / total) * 100) if total else 0,
        summary=_client_progress_summary(tasks, done),
    )

    return ClientSafeJobOrderStatus(
        vehicle_plate=job_order.vehicle.plate,
        vehicle_make=job_order.vehicle.make,
        vehicle_model=job_order.vehicle.model,
        vehicle_year=job_order.vehicle.year,
        overall_status_label=_friendly_job_order_status(job_order.status),
        overall_status_kind=job_order.status,
        progress=progress,
        jobs=jobs,
    )


def _friendly_job_order_status(status: str) -> str:
    labels = {
        JobOrderStatus.OPEN: "Vehiculo recibido",
        JobOrderStatus.IN_PROGRESS: "Trabajo en proceso",
        JobOrderStatus.DONE: "Trabajo terminado",
        JobOrderStatus.DELIVERED: "Vehiculo entregado",
    }
    return labels[status]


def _friendly_task_status(status: str) -> str:
    labels = {
        TaskStatus.PENDING: "Pendiente de inicio",
        TaskStatus.IN_PROGRESS: "En proceso",
        TaskStatus.COMPLETED: "Listo",
        TaskStatus.OVERDUE: "Requiere atencion",
        TaskStatus.CANCELLED: "No realizado",
    }
    return labels[status]


def _client_progress_summary(tasks: list, done: int) -> str:
    total = len(tasks)
    if total == 0:
        return "Vehiculo recibido. Prepararemos el diagnostico inicial."
    if done == total:
        return "Trabajo terminado. Coordinaremos la entrega del vehiculo."

    active_task = next(
        (task for task in tasks if task.status == TaskStatus.IN_PROGRESS),
        None,
    )
    if active_task:
        return f"{active_task.title} esta en proceso."

    ready_task = next(
        (task for task in tasks if task.status == TaskStatus.COMPLETED),
        None,
    )
    if ready_task:
        return f"{ready_task.title} esta listo; continuamos con el siguiente trabajo."

    return "Trabajo pendiente de inicio segun la programacion del taller."
