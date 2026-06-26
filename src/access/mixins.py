"""Reusable access-control mixins for internal views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from src.access.roles import (
    can_cancel_task,
    can_create_subtask,
    can_edit_task,
    can_update_task_status,
    can_view_job_order,
    can_view_task,
    has_role,
)


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles: tuple[str, ...] = ()

    def has_access(self) -> bool:
        return has_role(self.request.user, *self.allowed_roles)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.has_access():
            raise PermissionDenied("No tiene permiso para acceder a esta pagina.")
        return super().dispatch(request, *args, **kwargs)


class TaskObjectAccessMixin(LoginRequiredMixin):
    task_access_action = "view"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.object = self.get_object()
        allowed = {
            "view": can_view_task,
            "edit": can_edit_task,
            "status": can_update_task_status,
            "cancel": can_cancel_task,
        }[self.task_access_action](request.user, self.object)
        if not allowed:
            raise PermissionDenied("No tiene permiso para usar esta tarea.")
        return super().dispatch(request, *args, **kwargs)


class JobOrderObjectAccessMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.object = self.get_object()
        if not can_view_job_order(request.user, self.object):
            raise PermissionDenied("No tiene permiso para ver esta orden de trabajo.")
        return super().dispatch(request, *args, **kwargs)


class SubtaskParentAccessMixin(LoginRequiredMixin):
    def has_parent_access(self, parent_task) -> bool:
        return can_create_subtask(self.request.user, parent_task)
