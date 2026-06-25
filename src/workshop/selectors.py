"""Read/query helpers for the workshop module."""

from django.db.models import QuerySet

from src.workshop.models import JobOrder, JobOrderStatus


def job_orders_list() -> QuerySet[JobOrder]:
    return JobOrder.objects.select_related(
        "service_order__client",
        "vehicle",
    ).order_by("-interned_at")


def open_job_orders() -> QuerySet[JobOrder]:
    return job_orders_list().exclude(status=JobOrderStatus.DELIVERED)


def job_order_with_tasks(pk: int | str) -> JobOrder:
    return job_orders_list().prefetch_related("tasks__subtasks").get(pk=pk)
