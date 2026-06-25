"""Admin registrations for the workshop module."""

from django.contrib import admin

from src.workshop.models import JobOrder


@admin.register(JobOrder)
class JobOrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "service_order",
        "vehicle",
        "status",
        "interned_at",
        "closed_at",
    ]
    list_filter = ["status", "interned_at", "closed_at"]
    search_fields = [
        "id",
        "service_order__client__full_name",
        "vehicle__plate",
    ]
    autocomplete_fields = ["service_order", "vehicle"]
