"""Model tests for the sales module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrder


class ServiceOrderModelTests(TestCase):
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

    def test_service_order_defaults_to_open(self):
        order = ServiceOrder.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            description="Cambio de aceite y diagnostico.",
        )

        self.assertEqual(order.status, ServiceOrderStatus.OPEN)
        self.assertIn("Rosa Medina", str(order))


class ServiceOrderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.area = Area.objects.create(name="Recepcion")
        self.advisor = Employee.objects.create(
            full_name="Ana Torres",
            area=self.area,
            position="Asesora",
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

    def test_service_order_list_shows_client_vehicle_and_status(self):
        ServiceOrder.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            advisor=self.advisor,
            description="Revision general.",
            status=ServiceOrderStatus.APPROVED,
        )

        response = self.client.get(reverse("sales:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rosa Medina")
        self.assertContains(response, "ABC-123")
        self.assertContains(response, "Aprobada")

    def test_service_order_create_view_creates_order(self):
        response = self.client.post(
            reverse("sales:create"),
            {
                "client": self.client_obj.pk,
                "vehicle": self.vehicle.pk,
                "advisor": self.advisor.pk,
                "description": "Diagnostico inicial.",
                "status": ServiceOrderStatus.OPEN,
            },
        )

        self.assertRedirects(response, reverse("sales:list"))
        self.assertTrue(
            ServiceOrder.objects.filter(description="Diagnostico inicial.").exists()
        )

    def test_approved_service_order_create_generates_job_order(self):
        response = self.client.post(
            reverse("sales:create"),
            {
                "client": self.client_obj.pk,
                "vehicle": self.vehicle.pk,
                "advisor": self.advisor.pk,
                "description": "Diagnostico inicial.",
                "status": ServiceOrderStatus.APPROVED,
            },
        )

        self.assertRedirects(response, reverse("sales:list"))
        self.assertEqual(JobOrder.objects.count(), 1)
        self.assertEqual(JobOrder.objects.get().vehicle, self.vehicle)

    def test_approve_action_generates_job_order(self):
        order = ServiceOrder.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            description="Revision general.",
        )

        response = self.client.post(reverse("sales:approve", args=[order.pk]))

        job_order = JobOrder.objects.get()
        self.assertRedirects(response, reverse("workshop:detail", args=[job_order.pk]))
        order.refresh_from_db()
        self.assertEqual(order.status, ServiceOrderStatus.APPROVED)

    def test_service_order_form_rejects_vehicle_from_another_client(self):
        other_client = Client.objects.create(
            full_name="Luis Vargas",
            phone="988777666",
        )
        other_vehicle = Vehicle.objects.create(
            client=other_client,
            plate="XYZ-999",
            make="Nissan",
            model="Frontier",
            year=2021,
        )

        response = self.client.post(
            reverse("sales:create"),
            {
                "client": self.client_obj.pk,
                "vehicle": other_vehicle.pk,
                "advisor": "",
                "description": "Revision de frenos.",
                "status": ServiceOrderStatus.OPEN,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Seleccione un vehiculo que pertenezca al cliente.",
        )

    def test_service_order_update_view_updates_status(self):
        order = ServiceOrder.objects.create(
            client=self.client_obj,
            vehicle=self.vehicle,
            description="Revision general.",
        )

        response = self.client.post(
            reverse("sales:edit", args=[order.pk]),
            {
                "client": self.client_obj.pk,
                "vehicle": self.vehicle.pk,
                "advisor": self.advisor.pk,
                "description": "Revision general.",
                "status": ServiceOrderStatus.APPROVED,
            },
        )

        self.assertRedirects(response, reverse("sales:list"))
        order.refresh_from_db()
        self.assertEqual(order.status, ServiceOrderStatus.APPROVED)
