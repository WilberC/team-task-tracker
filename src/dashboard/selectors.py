"""Read-only dashboard snapshot helpers."""

from dataclasses import dataclass

from django.db.models import Count

from src.reports.selectors import (
    StatusCount,
    WorkloadCount,
    overdue_tasks,
    tasks_by_status,
    workload_by_assignee,
)
from src.tasks.models import Task, TaskPriority, TaskStatus
from src.workshop.models import JobOrder, JobOrderStatus


@dataclass(frozen=True)
class DashboardSnapshot:
    vehicles_in_shop: int
    status_counts: tuple[StatusCount, ...]
    overdue_count: int
    critical_count: int
    workload: tuple[WorkloadCount, ...]
    active_job_orders: int


def dashboard_snapshot() -> DashboardSnapshot:
    active_statuses = [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.OVERDUE]
    return DashboardSnapshot(
        vehicles_in_shop=JobOrder.objects.exclude(
            status=JobOrderStatus.DELIVERED
        ).count(),
        status_counts=tasks_by_status(),
        overdue_count=overdue_tasks().count(),
        critical_count=Task.objects.filter(
            priority=TaskPriority.CRITICAL,
            status__in=active_statuses,
        ).count(),
        workload=workload_by_assignee(),
        active_job_orders=JobOrder.objects.exclude(
            status=JobOrderStatus.DELIVERED
        ).count(),
    )


def current_area_load() -> tuple[dict, ...]:
    rows = (
        Task.objects.filter(
            status__in=[TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.OVERDUE]
        )
        .values("area__name")
        .annotate(count=Count("id"))
        .order_by("-count", "area__name")
    )
    return tuple({"area": row["area__name"], "count": row["count"]} for row in rows)
