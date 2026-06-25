"""Model tests for the workshop module."""

from django.test import TestCase
from django.urls import reverse

from src.clients.models import Client
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrder, JobOrderStatus
from src.workshop.selectors import open_job_orders
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
