"""Read/query helpers for the clients module."""

from django.db.models import QuerySet

from src.clients.models import Client


def clients_list() -> QuerySet[Client]:
    return Client.objects.order_by("full_name")
