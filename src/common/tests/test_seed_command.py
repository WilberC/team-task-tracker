"""Tests for the demo seed command."""

from io import StringIO

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings

from src.access.roles import ADMINISTRATOR, MECHANIC, ROLE_GROUPS
from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder
from src.tasks.models import Task, TaskStatus
from src.teams.models import Team
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrder, JobOrderStatus


@override_settings(SEED_USER_PASSWORD="ClaveSemilla123!")
class SeedCommandTests(TestCase):
    def call_seed(self, *args):
        output = StringIO()
        call_command("seed", *args, stdout=output)
        return output.getvalue()

    def test_seed_creates_roles_users_and_spanish_demo_data(self):
        output = self.call_seed()

        self.assertIn("Datos de prueba cargados", output)
        self.assertEqual(Group.objects.filter(name__in=ROLE_GROUPS).count(), 6)

        admin = User.objects.get(username="administrador")
        self.assertTrue(admin.check_password("ClaveSemilla123!"))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.groups.filter(name=ADMINISTRATOR).exists())

        mechanic = User.objects.get(username="mecanico")
        self.assertTrue(mechanic.groups.filter(name=MECHANIC).exists())
        self.assertEqual(mechanic.employee_profile.full_name, "Carlos Vargas")

        self.assertTrue(Area.objects.filter(name="Mecanica").exists())
        self.assertTrue(Client.objects.filter(full_name="Ana Maria Flores").exists())
        self.assertTrue(Vehicle.objects.filter(plate="ABC-123").exists())
        self.assertTrue(
            ServiceOrder.objects.filter(
                description__icontains="Revision general",
            ).exists()
        )
        self.assertTrue(
            JobOrder.objects.filter(status=JobOrderStatus.IN_PROGRESS).exists()
        )
        self.assertTrue(
            Task.objects.filter(
                title="Diagnostico de suspension delantera",
                status=TaskStatus.IN_PROGRESS,
            ).exists()
        )

    def test_seed_is_idempotent(self):
        self.call_seed()
        counts = self._counts()

        self.call_seed()

        self.assertEqual(self._counts(), counts)

    def test_seed_reset_reloads_known_records(self):
        self.call_seed()
        counts = self._counts()

        output = self.call_seed("--reset")

        self.assertIn("Usuarios de prueba", output)
        self.assertEqual(self._counts(), counts)
        self.assertTrue(Vehicle.objects.filter(plate="ABC-123").exists())
        self.assertEqual(User.objects.filter(username="administrador").count(), 1)

    def test_seed_password_argument_overrides_setting(self):
        self.call_seed("--password", "ClaveLocal456!")

        admin = User.objects.get(username="administrador")
        self.assertTrue(admin.check_password("ClaveLocal456!"))

    @override_settings(SEED_USER_PASSWORD="")
    def test_seed_requires_password_setting_or_argument(self):
        with self.assertRaisesMessage(
            CommandError,
            "Set SEED_USER_PASSWORD or pass --password.",
        ):
            self.call_seed()

    def _counts(self):
        return {
            "users": User.objects.count(),
            "employees": Employee.objects.count(),
            "areas": Area.objects.count(),
            "teams": Team.objects.count(),
            "clients": Client.objects.count(),
            "vehicles": Vehicle.objects.count(),
            "service_orders": ServiceOrder.objects.count(),
            "job_orders": JobOrder.objects.count(),
            "tasks": Task.objects.count(),
        }
