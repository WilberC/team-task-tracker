"""Access-control tests for internal roles."""

from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.access.roles import (
    FRONT_DESK,
    MECHANIC,
    REPORTS_VIEWER,
    ROLE_GROUPS,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
)
from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.tasks.models import TaskPriority, TaskStatus
from src.tasks.services import create_top_level_task
from src.vehicles.models import Vehicle
from src.workshop.services import generate_job_order


class RoleAccessTests(TestCase):
    def setUp(self):
        call_command("setup_roles")
        self.area = Area.objects.create(name="Mecanica")
        self.client_obj = Client.objects.create(
            full_name="Rosa Medina",
            phone="999111222",
        )
        self.vehicle = Vehicle.objects.create(
            client=self.client_obj,
            plate="ABC-123",
            make="Toyota",
            model="Corolla",
            year=2020,
        )
        self.service_order = ServiceOrder.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            description="Revision general.",
            status=ServiceOrderStatus.APPROVED,
        )
        self.job_order = generate_job_order(self.service_order)
        self.mechanic_user = self.user_with_role("mechanic", MECHANIC)
        self.other_mechanic_user = self.user_with_role("other-mechanic", MECHANIC)
        self.mechanic = Employee.objects.create(
            user=self.mechanic_user,
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )
        self.other_mechanic = Employee.objects.create(
            user=self.other_mechanic_user,
            full_name="Luis Vargas",
            area=self.area,
            position="Mecanico",
        )
        self.assigned_task = create_top_level_task(
            self.job_order,
            title="Diagnostico asignado",
            area=self.area,
            assigned_employee=self.mechanic,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate() + timedelta(days=1),
        )
        self.unrelated_task = create_top_level_task(
            self.job_order,
            title="Revision ajena",
            area=self.area,
            assigned_employee=self.other_mechanic,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate() + timedelta(days=1),
        )

    def user_with_role(self, username, role):
        user = User.objects.create_user(username=username, password="password")
        user.groups.add(Group.objects.get(name=role))
        return user

    def test_setup_roles_command_creates_all_groups(self):
        self.assertEqual(Group.objects.filter(name__in=ROLE_GROUPS).count(), 6)
        supervisor = Group.objects.get(name=WORKSHOP_SUPERVISOR)
        self.assertTrue(supervisor.permissions.filter(codename="change_task").exists())

    def test_internal_routes_redirect_anonymous_users_to_login(self):
        response = self.client.get(reverse("tasks:list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_public_client_status_stays_available_without_login(self):
        response = self.client.get(
            reverse("client_status", args=[self.job_order.client_status_token])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC-123")

    def test_root_page_redirects_to_login(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("login"))

    def test_login_without_next_uses_role_appropriate_target(self):
        self.client.force_login(self.mechanic_user)

        response = self.client.get(reverse("post_login"))

        self.assertRedirects(response, reverse("tasks:list"))

    def test_service_advisor_can_approve_service_order(self):
        advisor = self.user_with_role("advisor", SERVICE_ADVISOR)
        order = ServiceOrder.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            description="Cambio de aceite.",
        )
        self.client.force_login(advisor)

        response = self.client.post(reverse("sales:approve", args=[order.pk]))

        order.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.status, ServiceOrderStatus.APPROVED)

    def test_workshop_supervisor_can_close_job_order(self):
        supervisor = self.user_with_role("supervisor", WORKSHOP_SUPERVISOR)
        self.client.force_login(supervisor)

        response = self.client.post(reverse("workshop:close", args=[self.job_order.pk]))

        self.job_order.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(self.job_order.closed_at)

    def test_front_desk_cannot_close_job_order_by_direct_post(self):
        front_desk = self.user_with_role("front-desk", FRONT_DESK)
        self.client.force_login(front_desk)

        response = self.client.post(reverse("workshop:close", args=[self.job_order.pk]))

        self.assertEqual(response.status_code, 403)

    def test_reports_viewer_cannot_mutate_records_by_direct_post(self):
        reports_user = self.user_with_role("reports", REPORTS_VIEWER)
        self.client.force_login(reports_user)

        response = self.client.post(
            reverse("clients:create"),
            {"full_name": "Luis Vargas", "phone": "988777666", "email": ""},
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Client.objects.filter(full_name="Luis Vargas").exists())

    def test_mechanic_sees_only_assigned_tasks(self):
        self.client.force_login(self.mechanic_user)

        response = self.client.get(reverse("tasks:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diagnostico asignado")
        self.assertNotContains(response, "Revision ajena")

    def test_mechanic_cannot_open_unrelated_task(self):
        self.client.force_login(self.mechanic_user)

        response = self.client.get(
            reverse("tasks:detail", args=[self.unrelated_task.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_mechanic_can_update_assigned_task_status_only(self):
        self.client.force_login(self.mechanic_user)

        allowed = self.client.post(
            reverse("tasks:status", args=[self.assigned_task.pk]),
            {"status": TaskStatus.IN_PROGRESS},
            HTTP_ACCEPT="application/json",
        )
        denied = self.client.post(
            reverse("tasks:status", args=[self.unrelated_task.pk]),
            {"status": TaskStatus.IN_PROGRESS},
            HTTP_ACCEPT="application/json",
        )

        self.assigned_task.refresh_from_db()
        self.unrelated_task.refresh_from_db()
        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(self.assigned_task.status, TaskStatus.IN_PROGRESS)
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(self.unrelated_task.status, TaskStatus.PENDING)

    def test_mechanic_cannot_cancel_assigned_task(self):
        self.client.force_login(self.mechanic_user)

        response = self.client.post(
            reverse("tasks:cancel", args=[self.assigned_task.pk])
        )

        self.assigned_task.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.assigned_task.status, TaskStatus.PENDING)
