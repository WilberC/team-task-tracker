"""Admin registrations for the clients module."""

from django.contrib import admin

from src.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone", "email", "updated_at"]
    search_fields = ["full_name", "phone", "email"]
