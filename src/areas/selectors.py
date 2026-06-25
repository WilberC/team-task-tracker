"""Read/query helpers for the areas module."""

from django.db.models import QuerySet

from src.areas.models import Area


def active_areas() -> QuerySet[Area]:
    return Area.objects.filter(active=True).order_by("name")
