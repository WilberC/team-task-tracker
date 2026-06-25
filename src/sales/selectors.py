"""Read/query helpers for the sales module."""

from django.db.models import QuerySet

from src.sales.models import ServiceOrder


def service_orders_list() -> QuerySet[ServiceOrder]:
    return ServiceOrder.objects.select_related("client", "vehicle", "advisor").order_by(
        "-created_at"
    )
