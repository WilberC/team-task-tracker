"""Admin registrations for the sales module."""

from django.contrib import admin

from src.sales.models import ServiceOrder


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "vehicle",
        "advisor",
        "status",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = [
        "client__full_name",
        "vehicle__plate",
        "advisor__full_name",
        "description",
    ]
    autocomplete_fields = ["client", "vehicle", "advisor"]
