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

    if job_order.closed_at and job_order.status != JobOrderStatus.DONE:
        job_order.status = JobOrderStatus.DONE
        job_order.save(update_fields=["status", "updated_at"])
    return job_order
