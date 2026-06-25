"""Read/query helpers for the employees module."""

from django.db.models import QuerySet

from src.employees.models import Employee


def active_employees() -> QuerySet[Employee]:
    return (
        Employee.objects.select_related("area")
        .filter(active=True, area__active=True)
        .order_by("full_name")
    )


def active_employees_by_area(area_id: int | str) -> QuerySet[Employee]:
    return active_employees().filter(area_id=area_id)
