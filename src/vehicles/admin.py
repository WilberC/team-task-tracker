"""Admin registrations for the vehicles module."""

from django.contrib import admin

from src.vehicles.models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["plate", "client", "make", "model", "year", "updated_at"]
    list_filter = ["make", "year"]
    search_fields = ["plate", "make", "model", "client__full_name"]
    autocomplete_fields = ["client"]
