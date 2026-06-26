"""Model tests for the vehicles module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.clients.models import Client
from src.vehicles.models import Vehicle
from src.vehicles.selectors import vehicles_by_client


class VehicleModelTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            full_name="Rosa Medina",
            phone="999111222",
        )

    def test_vehicle_string_includes_plate_make_and_model(self):
        vehicle = Vehicle.objects.create(
            client=self.client_obj,
            plate="ABC-123",
            make="Toyota",
            model="Corolla",
            year=2020,
        )

        self.assertEqual(str(vehicle), "ABC-123 - Toyota Corolla")

    def test_vehicles_by_client_returns_only_client_vehicles(self):
        other_client = Client.objects.create(
            full_name="Luis Vargas",
            phone="988777666",
        )
        vehicle = Vehicle.objects.create(
            client=self.client_obj,
            plate="ABC-123",
            make="Toyota",
            model="Corolla",
            year=2020,
        )
        Vehicle.objects.create(
            client=other_client,
            plate="XYZ-999",
            make="Nissan",
            model="Frontier",
            year=2021,
        )

        self.assertQuerySetEqual(vehicles_by_client(self.client_obj.pk), [vehicle])


class VehicleViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.client_obj = Client.objects.create(
            full_name="Rosa Medina",
            phone="999111222",
        )

    def test_vehicle_list_renders_registered_vehicles(self):
        Vehicle.objects.create(
            client=self.client_obj,
            plate="ABC-123",
            make="Toyota",
            model="Corolla",
            year=2020,
        )

        response = self.client.get(reverse("vehicles:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ABC-123")

    def test_vehicle_create_view_creates_vehicle(self):
        response = self.client.post(
            reverse("vehicles:create"),
            {
                "client": self.client_obj.pk,
                "plate": "abc-123",
                "make": "Toyota",
                "model": "Corolla",
                "year": 2020,
            },
        )

        self.assertRedirects(response, reverse("vehicles:list"))
        self.assertTrue(Vehicle.objects.filter(plate="ABC-123").exists())

    def test_vehicle_update_view_updates_vehicle(self):
        vehicle = Vehicle.objects.create(
            client=self.client_obj,
            plate="ABC-123",
            make="Toyota",
            model="Corolla",
            year=2020,
        )

        response = self.client.post(
            reverse("vehicles:edit", args=[vehicle.pk]),
            {
                "client": self.client_obj.pk,
                "plate": "ABC-123",
                "make": "Toyota",
                "model": "Hilux",
                "year": 2022,
            },
        )

        self.assertRedirects(response, reverse("vehicles:list"))
        vehicle.refresh_from_db()
        self.assertEqual(vehicle.model, "Hilux")
