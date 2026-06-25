"""Functional report aggregations for task data."""

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from django.db.models import QuerySet
from django.utils import timezone

from src.tasks.models import Task, TaskStatus


@dataclass(frozen=True)
class StatusCount:
    status: str
    label: str
    count: int


@dataclass(frozen=True)
class WorkloadCount:
    assignee: str
    kind: str
    count: int


@dataclass(frozen=True)
class AreaProductivity:
    area: str
    completed: int


@dataclass(frozen=True)
class DeadlineCompliance:
    on_time_count: int
    late_count: int
    on_time_percent: int
    late_percent: int


def report_tasks_queryset() -> QuerySet[Task]:
    return Task.objects.select_related(
        "area",
        "assigned_employee",
        "assigned_team",
        "job_order__vehicle",
    )


def tasks_by_status(tasks: Iterable[Task] | None = None) -> tuple[StatusCount, ...]:
    task_items = list(tasks if tasks is not None else report_tasks_queryset())
    counts = Counter(task.status for task in task_items)
    return tuple(
        StatusCount(status=status, label=label, count=counts.get(status, 0))
        for status, label in TaskStatus.choices
    )


def overdue_tasks(today: date | None = None) -> QuerySet[Task]:
    current_day = today or timezone.localdate()
    return (
        report_tasks_queryset()
        .filter(
            due_date__lt=current_day,
            status__in=[
                TaskStatus.PENDING,
                TaskStatus.IN_PROGRESS,
                TaskStatus.OVERDUE,
            ],
        )
        .order_by("due_date", "priority", "title")
    )


def workload_by_assignee(
    tasks: Iterable[Task] | None = None,
) -> tuple[WorkloadCount, ...]:
    task_items = [
        task
        for task in list(tasks if tasks is not None else report_tasks_queryset())
        if task.status not in {TaskStatus.COMPLETED, TaskStatus.CANCELLED}
    ]
    counts = Counter(_assignee_key(task) for task in task_items)
    return tuple(
        WorkloadCount(assignee=assignee, kind=kind, count=count)
        for (kind, assignee), count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0][1]),
        )
    )


def productivity_by_area(
    start_date: date,
    end_date: date,
    tasks: Iterable[Task] | None = None,
) -> tuple[AreaProductivity, ...]:
    task_items = [
        task
        for task in list(tasks if tasks is not None else report_tasks_queryset())
        if task.status == TaskStatus.COMPLETED
        and task.completion_date
        and start_date <= task.completion_date <= end_date
    ]
    counts = Counter(task.area.name for task in task_items)
    return tuple(
        AreaProductivity(area=area, completed=count)
        for area, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    )


def deadline_compliance(
    start_date: date,
    end_date: date,
    tasks: Iterable[Task] | None = None,
) -> DeadlineCompliance:
    task_items = [
        task
        for task in list(tasks if tasks is not None else report_tasks_queryset())
        if task.status == TaskStatus.COMPLETED
        and task.completion_date
        and start_date <= task.completion_date <= end_date
    ]
    total = len(task_items)
    on_time = sum(1 for task in task_items if task.completion_date <= task.due_date)
    late = total - on_time
    return DeadlineCompliance(
        on_time_count=on_time,
        late_count=late,
        on_time_percent=round((on_time / total) * 100) if total else 0,
        late_percent=round((late / total) * 100) if total else 0,
    )


def _assignee_key(task: Task) -> tuple[str, str]:
    if task.assigned_employee_id:
        return ("Empleado", task.assigned_employee.full_name)
    return ("Equipo", task.assigned_team.name)
