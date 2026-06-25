"""Service tests for the sales module."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from src.clients.models import Client
from src.sales.models import ServiceOrderStatus
from src.sales.services import create_service_order
from src.vehicles.models import Vehicle


class CreateServiceOrderTests(TestCase):
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

    def test_create_service_order_persists_order(self):
        order = create_service_order(
            client=self.client_obj,
            vehicle=self.vehicle,
            description="Diagnostico inicial.",
        )

        self.assertEqual(order.status, ServiceOrderStatus.OPEN)
        self.assertEqual(order.client, self.client_obj)
        self.assertEqual(order.vehicle, self.vehicle)

    def test_create_service_order_rejects_mismatched_vehicle(self):
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

        with self.assertRaises(ValidationError):
            create_service_order(
                client=self.client_obj,
                vehicle=other_vehicle,
                description="Revision.",
            )
