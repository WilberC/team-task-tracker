"""Read/query helpers for the tasks module."""

from dataclasses import dataclass
from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone

from src.tasks.models import Task, TaskStatus


@dataclass(frozen=True)
class TaskProgress:
    total: int
    done: int
    percent: int
    at_risk: bool


def tasks_list(filters: dict | None = None) -> QuerySet[Task]:
    queryset = (
        Task.objects.select_related(
            "job_order__vehicle",
            "parent_task",
            "area",
            "assigned_employee",
            "assigned_team",
        )
        .prefetch_related("assigned_team__members")
        .order_by("due_date", "title")
    )
    if not filters:
        return queryset

    filter_map = {
        "job_order": "job_order_id",
        "area": "area_id",
        "assigned_employee": "assigned_employee_id",
        "assigned_team": "assigned_team_id",
        "status": "status",
        "priority": "priority",
        "due_date": "due_date",
    }
    for key, lookup in filter_map.items():
        value = filters.get(key)
        if value:
            queryset = queryset.filter(**{lookup: value})
    if filters.get("due_this_week"):
        today = timezone.localdate()
        queryset = queryset.filter(due_date__range=(today, today + timedelta(days=7)))
    return queryset


def top_level_tasks_for_job_order(job_order_id: int | str) -> QuerySet[Task]:
    return tasks_list().filter(job_order_id=job_order_id, parent_task__isnull=True)


def task_with_subtasks(pk: int | str) -> Task:
    return (
        tasks_list()
        .prefetch_related(
            "subtasks__area",
            "subtasks__assigned_employee",
            "subtasks__assigned_team",
            "subtasks__assigned_team__members",
        )
        .get(pk=pk)
    )


def subtask_progress(parent_task: Task) -> TaskProgress:
    subtasks = parent_task.subtasks.all()
    total = subtasks.count()
    if total == 0:
        return TaskProgress(total=0, done=0, percent=0, at_risk=False)

    done = subtasks.filter(
        status__in=[TaskStatus.COMPLETED, TaskStatus.CANCELLED]
    ).count()
    at_risk = subtasks.filter(status=TaskStatus.OVERDUE).exists()
    return TaskProgress(
        total=total,
        done=done,
        percent=round((done / total) * 100),
        at_risk=at_risk,
    )


def kanban_columns(filters: dict | None = None) -> dict[str, QuerySet[Task]]:
    queryset = tasks_list(filters).filter(parent_task__isnull=True)
    return {
        status: queryset.filter(status=status) for status, _label in TaskStatus.choices
    }
