"""Admin registrations for the teams module."""

from django.contrib import admin

from src.teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name", "area", "active", "updated_at"]
    list_filter = ["active", "area"]
    search_fields = ["name", "members__full_name"]
    autocomplete_fields = ["area", "members"]
    filter_horizontal = ["members"]
