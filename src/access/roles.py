"""Role names and permission helpers for internal users."""

from dataclasses import dataclass

from django.contrib.auth.models import Group, User
from django.db.models import Q

from src.tasks.models import Task
from src.workshop.models import JobOrder

ADMINISTRATOR = "Administrator"
FRONT_DESK = "Front desk"
SERVICE_ADVISOR = "Service advisor"
WORKSHOP_SUPERVISOR = "Workshop supervisor"
MECHANIC = "Mechanic"
REPORTS_VIEWER = "Reports viewer"

ROLE_GROUPS = (
    ADMINISTRATOR,
    FRONT_DESK,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
    MECHANIC,
    REPORTS_VIEWER,
)


@dataclass(frozen=True)
class AccessFlags:
    can_view_clients: bool
    can_edit_clients: bool
    can_view_vehicles: bool
    can_edit_vehicles: bool
    can_view_sales: bool
    can_edit_sales: bool
    can_approve_service_orders: bool
    can_view_workshop: bool
    can_manage_job_orders: bool
    can_view_tasks: bool
    can_manage_tasks: bool
    can_view_dashboard: bool
    can_view_reports: bool
    can_view_people: bool
    can_manage_people: bool
    can_access_admin: bool


def ensure_default_groups() -> tuple[Group, ...]:
    return tuple(Group.objects.get_or_create(name=name)[0] for name in ROLE_GROUPS)


def has_role(user: User, *roles: str) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=roles).exists()


def is_administrator(user: User) -> bool:
    return has_role(user, ADMINISTRATOR)


def employee_for_user(user: User):
    if not user.is_authenticated:
        return None
    return getattr(user, "employee_profile", None)


def access_flags(user: User) -> AccessFlags:
    can_view_front_desk = has_role(
        user,
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    )
    can_edit_front_desk = has_role(user, ADMINISTRATOR, FRONT_DESK, SERVICE_ADVISOR)
    can_view_workshop = has_role(
        user,
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        MECHANIC,
        REPORTS_VIEWER,
    )
    can_manage_tasks = has_role(user, ADMINISTRATOR, WORKSHOP_SUPERVISOR)
    return AccessFlags(
        can_view_clients=can_view_front_desk,
        can_edit_clients=can_edit_front_desk,
        can_view_vehicles=can_view_front_desk,
        can_edit_vehicles=can_edit_front_desk,
        can_view_sales=can_view_front_desk,
        can_edit_sales=can_edit_front_desk,
        can_approve_service_orders=has_role(user, ADMINISTRATOR, SERVICE_ADVISOR),
        can_view_workshop=can_view_workshop,
        can_manage_job_orders=has_role(user, ADMINISTRATOR, WORKSHOP_SUPERVISOR),
        can_view_tasks=has_role(
            user,
            ADMINISTRATOR,
            SERVICE_ADVISOR,
            WORKSHOP_SUPERVISOR,
            MECHANIC,
            REPORTS_VIEWER,
        ),
        can_manage_tasks=can_manage_tasks,
        can_view_dashboard=has_role(
            user,
            ADMINISTRATOR,
            SERVICE_ADVISOR,
            WORKSHOP_SUPERVISOR,
            REPORTS_VIEWER,
        ),
        can_view_reports=has_role(
            user,
            ADMINISTRATOR,
            WORKSHOP_SUPERVISOR,
            REPORTS_VIEWER,
        ),
        can_view_people=has_role(
            user,
            ADMINISTRATOR,
            SERVICE_ADVISOR,
            WORKSHOP_SUPERVISOR,
            REPORTS_VIEWER,
        ),
        can_manage_people=has_role(user, ADMINISTRATOR),
        can_access_admin=has_role(user, ADMINISTRATOR),
    )


def can_view_task(user: User, task: Task) -> bool:
    if has_role(
        user, ADMINISTRATOR, SERVICE_ADVISOR, WORKSHOP_SUPERVISOR, REPORTS_VIEWER
    ):
        return True
    employee = employee_for_user(user)
    if not employee or not has_role(user, MECHANIC):
        return False
    return _task_is_assigned_to_employee(task, employee)


def can_update_task_status(user: User, task: Task) -> bool:
    if has_role(user, ADMINISTRATOR, WORKSHOP_SUPERVISOR):
        return True
    employee = employee_for_user(user)
    return bool(
        employee
        and has_role(user, MECHANIC)
        and _task_is_assigned_to_employee(task, employee)
    )


def can_create_subtask(user: User, parent_task: Task) -> bool:
    if has_role(user, ADMINISTRATOR, WORKSHOP_SUPERVISOR):
        return True
    employee = employee_for_user(user)
    return bool(
        employee
        and has_role(user, MECHANIC)
        and parent_task.is_top_level
        and _task_is_assigned_to_employee(parent_task, employee)
    )


def can_edit_task(user: User, task: Task) -> bool:
    if has_role(user, ADMINISTRATOR, WORKSHOP_SUPERVISOR):
        return True
    employee = employee_for_user(user)
    return bool(
        employee
        and has_role(user, MECHANIC)
        and task.is_subtask
        and _task_is_assigned_to_employee(task.parent_task, employee)
    )


def can_cancel_task(user: User, task: Task) -> bool:
    return has_role(user, ADMINISTRATOR, WORKSHOP_SUPERVISOR)


def can_view_job_order(user: User, job_order: JobOrder) -> bool:
    if has_role(
        user,
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    ):
        return True
    employee = employee_for_user(user)
    if not employee or not has_role(user, MECHANIC):
        return False
    return job_order.tasks.filter(
        Q(assigned_employee=employee)
        | Q(assigned_team__members=employee)
        | Q(subtasks__assigned_employee=employee)
        | Q(subtasks__assigned_team__members=employee)
    ).exists()


def task_queryset_for_user(user: User):
    queryset = Task.objects.all()
    if has_role(
        user, ADMINISTRATOR, SERVICE_ADVISOR, WORKSHOP_SUPERVISOR, REPORTS_VIEWER
    ):
        return queryset
    employee = employee_for_user(user)
    if not employee or not has_role(user, MECHANIC):
        return queryset.none()
    return queryset.filter(
        Q(assigned_employee=employee)
        | Q(assigned_team__members=employee)
        | Q(parent_task__assigned_employee=employee)
        | Q(parent_task__assigned_team__members=employee)
    ).distinct()


def job_order_queryset_for_user(user: User):
    queryset = JobOrder.objects.all()
    if has_role(
        user,
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    ):
        return queryset
    employee = employee_for_user(user)
    if not employee or not has_role(user, MECHANIC):
        return queryset.none()
    return queryset.filter(
        Q(tasks__assigned_employee=employee)
        | Q(tasks__assigned_team__members=employee)
        | Q(tasks__subtasks__assigned_employee=employee)
        | Q(tasks__subtasks__assigned_team__members=employee)
    ).distinct()


def _task_is_assigned_to_employee(task: Task, employee) -> bool:
    if task.assigned_employee_id == employee.pk:
        return True
    if task.assigned_team_id:
        return task.assigned_team.members.filter(pk=employee.pk).exists()
    return False
