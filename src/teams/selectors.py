"""Read/query helpers for the teams module."""

from django.db.models import QuerySet

from src.teams.models import Team


def active_teams() -> QuerySet[Team]:
    return (
        Team.objects.select_related("area")
        .prefetch_related("members")
        .filter(active=True, area__active=True)
        .order_by("name")
    )


def active_teams_by_area(area_id: int | str) -> QuerySet[Team]:
    return active_teams().filter(area_id=area_id)
