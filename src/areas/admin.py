"""Admin registrations for the areas module."""

from django.contrib import admin

from src.areas.models import Area


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "updated_at"]
    list_filter = ["active"]
    search_fields = ["name", "description"]
