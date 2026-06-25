"""Write orchestration for the workshop module."""

from django.db import transaction
from django.utils import timezone

from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.workshop.models import JobOrder, JobOrderStatus


@transaction.atomic
def generate_job_order(service_order: ServiceOrder) -> JobOrder:
    if service_order.status != ServiceOrderStatus.APPROVED:
        service_order.status = ServiceOrderStatus.APPROVED
        service_order.save(update_fields=["status", "updated_at"])

    job_order, _created = JobOrder.objects.get_or_create(
        service_order=service_order,
        defaults={
            "vehicle": service_order.vehicle,
            "status": JobOrderStatus.OPEN,
            "interned_at": timezone.now(),
        },
    )
    return job_order


def close_job_order(job_order: JobOrder) -> JobOrder:
    job_order.status = JobOrderStatus.DONE
    job_order.closed_at = timezone.now()
    job_order.save(update_fields=["status", "closed_at", "updated_at"])
    return job_order


def mark_job_order_delivered(job_order: JobOrder) -> JobOrder:
    job_order.status = JobOrderStatus.DELIVERED
    if job_order.closed_at is None:
        job_order.closed_at = timezone.now()
    job_order.save(update_fields=["status", "closed_at", "updated_at"])
    return job_order


def refresh_job_order_status(job_order: JobOrder) -> JobOrder:
    if job_order.status == JobOrderStatus.DELIVERED:
        return job_order

    from src.tasks.models import TaskStatus

    top_level_tasks = job_order.tasks.filter(parent_task__isnull=True)
    if not top_level_tasks.exists():
        next_status = JobOrderStatus.OPEN
    elif not top_level_tasks.exclude(
        status__in=[TaskStatus.COMPLETED, TaskStatus.CANCELLED]
    ).exists():
        next_status = JobOrderStatus.DONE
    elif top_level_tasks.exclude(status=TaskStatus.PENDING).exists():
        next_status = JobOrderStatus.IN_PROGRESS
    else:
        next_status = JobOrderStatus.OPEN

    update_fields = ["status", "updated_at"]
    job_order.status = next_status
    if next_status == JobOrderStatus.DONE and job_order.closed_at is None:
        job_order.closed_at = timezone.now()
        update_fields.append("closed_at")
    elif next_status != JobOrderStatus.DONE and job_order.closed_at is not None:
        job_order.closed_at = None
        update_fields.append("closed_at")
    job_order.save(update_fields=update_fields)
    return job_order
