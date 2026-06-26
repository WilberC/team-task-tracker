"""Model tests for the workshop module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.tasks.models import TaskPriority, TaskStatus
from src.tasks.services import create_top_level_task, update_status
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrder, JobOrderStatus
from src.workshop.selectors import client_safe_job_order_status, open_job_orders
from src.workshop.services import (
    close_job_order,
    generate_job_order,
    mark_job_order_delivered,
)


class JobOrderModelTests(TestCase):
    def setUp(self):
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

    def test_job_order_string_uses_id_and_plate(self):
        job_order = generate_job_order(self.service_order)

        self.assertEqual(str(job_order), f"OT-{job_order.pk} - ABC-123")

    def test_generate_job_order_creates_exactly_one_job_order(self):
        first = generate_job_order(self.service_order)
        second = generate_job_order(self.service_order)

        self.assertEqual(first, second)
        self.assertEqual(JobOrder.objects.count(), 1)
        self.assertIsNotNone(first.client_status_token)

    def test_generate_job_order_approves_open_service_order(self):
        self.service_order.status = ServiceOrderStatus.OPEN
        self.service_order.save(update_fields=["status"])

        job_order = generate_job_order(self.service_order)

        self.service_order.refresh_from_db()
        self.assertEqual(self.service_order.status, ServiceOrderStatus.APPROVED)
        self.assertEqual(job_order.vehicle, self.vehicle)

    def test_close_and_deliver_job_order_transitions_status(self):
        job_order = generate_job_order(self.service_order)

        close_job_order(job_order)
        job_order.refresh_from_db()
        self.assertEqual(job_order.status, JobOrderStatus.DONE)
        self.assertIsNotNone(job_order.closed_at)

        mark_job_order_delivered(job_order)
        job_order.refresh_from_db()
        self.assertEqual(job_order.status, JobOrderStatus.DELIVERED)

    def test_open_job_orders_excludes_delivered_orders(self):
        job_order = generate_job_order(self.service_order)
        delivered = mark_job_order_delivered(job_order)

        self.assertNotIn(delivered, open_job_orders())


class JobOrderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.area = Area.objects.create(name="Mecanica")
        self.advisor = Employee.objects.create(
            full_name="Luis Asesor",
            area=self.area,
            position="Asesor",
        )
        self.mechanic = Employee.objects.create(
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )
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
            advisor=self.advisor,
            description="Revision general.",
            status=ServiceOrderStatus.APPROVED,
        )
        self.job_order = generate_job_order(self.service_order)

    def test_job_order_list_renders_open_job_order(self):
        response = self.client.get(reverse("workshop:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"OT-{self.job_order.pk}")
        self.assertContains(response, "ABC-123")

    def test_job_order_detail_renders_client_vehicle_and_status(self):
        response = self.client.get(reverse("workshop:detail", args=[self.job_order.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rosa Medina")
        self.assertContains(response, "ABC-123")
        self.assertContains(response, "Abierta")

    def test_close_job_order_action_closes_order(self):
        response = self.client.post(reverse("workshop:close", args=[self.job_order.pk]))

        self.assertRedirects(
            response,
            reverse("workshop:detail", args=[self.job_order.pk]),
        )
        self.job_order.refresh_from_db()
        self.assertEqual(self.job_order.status, JobOrderStatus.DONE)

    def test_deliver_job_order_action_marks_delivered(self):
        response = self.client.post(
            reverse("workshop:deliver", args=[self.job_order.pk])
        )

        self.assertRedirects(response, reverse("workshop:list"))
        self.job_order.refresh_from_db()
        self.assertEqual(self.job_order.status, JobOrderStatus.DELIVERED)

    def test_client_status_view_resolves_token_without_login(self):
        self.client.logout()
        response = self.client.get(
            reverse("client_status", args=[self.job_order.client_status_token])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC-123")
        self.assertContains(response, "Toyota Corolla")
        self.assertContains(response, "Vehiculo recibido")

    def test_client_status_view_returns_404_for_invalid_token(self):
        self.client.logout()
        response = self.client.get(
            reverse("client_status", args=["11111111-1111-1111-1111-111111111111"])
        )

        self.assertEqual(response.status_code, 404)

    def test_client_status_view_exposes_only_client_safe_fields(self):
        task = create_top_level_task(
            self.job_order,
            title="Diagnostico inicial",
            area=self.area,
            assigned_employee=self.mechanic,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate(),
        )
        update_status(task, TaskStatus.IN_PROGRESS)
        self.client.logout()

        response = self.client.get(
            reverse("client_status", args=[self.job_order.client_status_token])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diagnostico inicial")
        self.assertContains(response, "En proceso")
        self.assertNotContains(response, "Rosa Medina")
        self.assertNotContains(response, "Luis Asesor")
        self.assertNotContains(response, "Carlos Ramos")
        self.assertNotContains(response, "Revision general.")

    def test_client_safe_selector_returns_progress_without_internal_data(self):
        task = create_top_level_task(
            self.job_order,
            title="Revision de frenos",
            area=self.area,
            assigned_employee=self.mechanic,
            priority=TaskPriority.HIGH,
            due_date=timezone.localdate(),
        )
        update_status(task, TaskStatus.IN_PROGRESS)
        update_status(task, TaskStatus.COMPLETED)

        snapshot = client_safe_job_order_status(self.job_order.client_status_token)

        self.assertEqual(snapshot.vehicle_plate, "ABC-123")
        self.assertEqual(snapshot.progress.done, 1)
        self.assertEqual(snapshot.progress.percent, 100)
        self.assertEqual(snapshot.jobs[0].title, "Revision de frenos")
