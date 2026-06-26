"""Role-aware template filters."""

from django import template

from src.access.roles import (
    can_cancel_task,
    can_create_subtask,
    can_edit_task,
    can_update_task_status,
)

register = template.Library()


@register.filter
def can_update_task(user, task) -> bool:
    return can_update_task_status(user, task)


@register.filter
def can_edit_task_object(user, task) -> bool:
    return can_edit_task(user, task)


@register.filter
def can_cancel_task_object(user, task) -> bool:
    return can_cancel_task(user, task)


@register.filter
def can_add_subtask(user, task) -> bool:
    return can_create_subtask(user, task)
