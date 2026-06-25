"""Read/query helpers for the vehicles module."""

from django.db.models import QuerySet

from src.vehicles.models import Vehicle


def vehicles_list() -> QuerySet[Vehicle]:
    return Vehicle.objects.select_related("client").order_by("plate")


def vehicles_by_client(client_id: int | str) -> QuerySet[Vehicle]:
    return vehicles_list().filter(client_id=client_id)
