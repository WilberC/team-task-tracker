"""Admin registrations for the employees module."""

from django.contrib import admin

from src.employees.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["full_name", "position", "area", "active", "updated_at"]
    list_filter = ["active", "area"]
    search_fields = ["full_name", "email", "position"]
    autocomplete_fields = ["area"]
