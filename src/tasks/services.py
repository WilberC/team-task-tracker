"""Write orchestration for the tasks module."""

from django.core.exceptions import ValidationError
from django.utils import timezone

from src.employees.models import Employee
from src.tasks.models import Task, TaskStatus
from src.teams.models import Team
from src.workshop.models import JobOrder
from src.workshop.services import refresh_job_order_status

ALLOWED_TRANSITIONS = {
    TaskStatus.PENDING: {
        TaskStatus.IN_PROGRESS,
        TaskStatus.OVERDUE,
        TaskStatus.CANCELLED,
    },
    TaskStatus.IN_PROGRESS: {
        TaskStatus.COMPLETED,
        TaskStatus.OVERDUE,
        TaskStatus.CANCELLED,
    },
    TaskStatus.OVERDUE: {
        TaskStatus.COMPLETED,
        TaskStatus.CANCELLED,
    },
    TaskStatus.COMPLETED: set(),
    TaskStatus.CANCELLED: set(),
}


def create_top_level_task(job_order: JobOrder, **data) -> Task:
    task = Task(
        job_order=job_order,
        parent_task=None,
        status=TaskStatus.PENDING,
        **data,
    )
    task.save()
    refresh_job_order_status(job_order)
    return task


def create_subtask(parent_task: Task, **data) -> Task:
    task = Task(
        parent_task=parent_task,
        job_order=None,
        area=data.pop("area", None) or parent_task.area,
        status=TaskStatus.PENDING,
        **data,
    )
    task.save()
    refresh_parent_progress(parent_task)
    return task


def assign_task(
    task: Task,
    *,
    employee: Employee | None = None,
    team: Team | None = None,
) -> Task:
    task.assigned_employee = employee
    task.assigned_team = team
    task.save()
    return task


def update_status(task: Task, new_status: str) -> Task:
    if new_status == task.status:
        return task

    if new_status not in ALLOWED_TRANSITIONS[task.status]:
        raise ValidationError("Este cambio de estado no esta permitido.")

    task.status = new_status
    if new_status == TaskStatus.COMPLETED:
        task.completion_date = timezone.localdate()
    elif new_status != TaskStatus.COMPLETED:
        task.completion_date = None
    task.save(update_fields=["status", "completion_date", "updated_at"])

    if task.parent_task_id:
        refresh_parent_progress(task.parent_task)
    elif task.job_order_id:
        refresh_job_order_status(task.job_order)
    return task


def cancel_task(task: Task) -> Task:
    return update_status(task, TaskStatus.CANCELLED)


def mark_overdue_tasks(today=None) -> int:
    today = today or timezone.localdate()
    tasks = Task.objects.filter(
        due_date__lt=today,
        status__in=[TaskStatus.PENDING, TaskStatus.IN_PROGRESS],
    )
    count = 0
    for task in tasks:
        update_status(task, TaskStatus.OVERDUE)
        count += 1
    return count


def refresh_parent_progress(parent_task: Task) -> Task:
    subtasks = parent_task.subtasks.all()
    if not subtasks.exists():
        return parent_task

    all_done = not subtasks.exclude(
        status__in=[TaskStatus.COMPLETED, TaskStatus.CANCELLED]
    ).exists()
    if all_done and parent_task.status != TaskStatus.COMPLETED:
        parent_task.status = TaskStatus.COMPLETED
        parent_task.completion_date = timezone.localdate()
        parent_task.save(update_fields=["status", "completion_date", "updated_at"])

    if parent_task.job_order_id:
        refresh_job_order_status(parent_task.job_order)
    return parent_task
