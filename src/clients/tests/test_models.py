"""Model tests for the clients module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.clients.models import Client


class ClientModelTests(TestCase):
    def test_client_string_uses_full_name(self):
        client = Client.objects.create(
            full_name="Rosa Medina",
            phone="999111222",
        )

        self.assertEqual(str(client), "Rosa Medina")


class ClientViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)

    def test_client_list_renders_registered_clients(self):
        Client.objects.create(full_name="Rosa Medina", phone="999111222")

        response = self.client.get(reverse("clients:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rosa Medina")

    def test_client_create_view_creates_client(self):
        response = self.client.post(
            reverse("clients:create"),
            {
                "full_name": "Luis Vargas",
                "phone": "988777666",
                "email": "luis@example.com",
            },
        )

        self.assertRedirects(response, reverse("clients:list"))
        self.assertTrue(Client.objects.filter(full_name="Luis Vargas").exists())

    def test_client_update_view_updates_client(self):
        client = Client.objects.create(full_name="Rosa Medina", phone="999111222")

        response = self.client.post(
            reverse("clients:edit", args=[client.pk]),
            {
                "full_name": "Rosa M. Medina",
                "phone": "999111222",
                "email": "",
            },
        )

        self.assertRedirects(response, reverse("clients:list"))
        client.refresh_from_db()
        self.assertEqual(client.full_name, "Rosa M. Medina")
