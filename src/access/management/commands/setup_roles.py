"""Create the default access-control groups."""

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from src.access.roles import (
    ADMINISTRATOR,
    FRONT_DESK,
    MECHANIC,
    REPORTS_VIEWER,
    ROLE_GROUPS,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
    ensure_default_groups,
)
from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder
from src.tasks.models import Task
from src.teams.models import Team
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrder

ROLE_PERMISSION_MAP = {
    ADMINISTRATOR: {
        Client: ["view", "add", "change"],
        Vehicle: ["view", "add", "change"],
        ServiceOrder: ["view", "add", "change"],
        JobOrder: ["view", "add", "change"],
        Task: ["view", "add", "change"],
        Area: ["view", "add", "change"],
        Employee: ["view", "add", "change"],
        Team: ["view", "add", "change"],
    },
    FRONT_DESK: {
        Client: ["view", "add", "change"],
        Vehicle: ["view", "add", "change"],
        ServiceOrder: ["view", "add", "change"],
        JobOrder: ["view"],
    },
    SERVICE_ADVISOR: {
        Client: ["view", "add", "change"],
        Vehicle: ["view", "add", "change"],
        ServiceOrder: ["view", "add", "change"],
        JobOrder: ["view"],
        Task: ["view"],
        Area: ["view"],
        Employee: ["view"],
        Team: ["view"],
    },
    WORKSHOP_SUPERVISOR: {
        Client: ["view"],
        Vehicle: ["view"],
        ServiceOrder: ["view"],
        JobOrder: ["view", "change"],
        Task: ["view", "add", "change"],
        Area: ["view"],
        Employee: ["view"],
        Team: ["view"],
    },
    MECHANIC: {
        JobOrder: ["view"],
        Task: ["view", "add", "change"],
    },
    REPORTS_VIEWER: {
        Client: ["view"],
        Vehicle: ["view"],
        ServiceOrder: ["view"],
        JobOrder: ["view"],
        Task: ["view"],
        Area: ["view"],
        Employee: ["view"],
        Team: ["view"],
    },
}


class Command(BaseCommand):
    help = "Create default role groups for internal access control."

    def handle(self, *args, **options):
        groups = {group.name: group for group in ensure_default_groups()}
        for role, model_permissions in ROLE_PERMISSION_MAP.items():
            group = groups[role]
            group.permissions.set(_permissions_for_models(model_permissions))
        self.stdout.write(
            self.style.SUCCESS(f"Configured {len(ROLE_GROUPS)} role groups.")
        )


def _permissions_for_models(model_permissions):
    permissions = []
    for model, actions in model_permissions.items():
        content_type = ContentType.objects.get_for_model(model)
        codenames = [f"{action}_{model._meta.model_name}" for action in actions]
        permissions.extend(
            Permission.objects.filter(
                content_type=content_type,
                codename__in=codenames,
            )
        )
    return permissions
