"""Admin registrations for the tasks module."""

from django.contrib import admin

from src.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "job_order",
        "parent_task",
        "area",
        "status",
        "priority",
        "due_date",
    ]
    list_filter = ["status", "priority", "area", "due_date"]
    search_fields = [
        "title",
        "description",
        "job_order__id",
        "assigned_employee__full_name",
        "assigned_team__name",
    ]
    autocomplete_fields = [
        "job_order",
        "parent_task",
        "area",
        "assigned_employee",
        "assigned_team",
    ]
