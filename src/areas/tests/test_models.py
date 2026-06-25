"""Model tests for the areas module."""

from django.test import TestCase
from django.urls import reverse

from src.areas.models import Area
from src.areas.selectors import active_areas


class AreaModelTests(TestCase):
    def test_area_string_uses_name(self):
        area = Area.objects.create(name="Mecanica", description="Linea principal")

        self.assertEqual(str(area), "Mecanica")

    def test_active_areas_selector_excludes_inactive_areas(self):
        active = Area.objects.create(name="Pintura")
        inactive = Area.objects.create(name="Archivo", active=False)

        areas = active_areas()

        self.assertIn(active, areas)
        self.assertNotIn(inactive, areas)


class AreaViewTests(TestCase):
    def test_area_list_renders_registered_areas(self):
        Area.objects.create(name="Electricidad")

        response = self.client.get(reverse("areas:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Electricidad")

    def test_area_create_view_creates_area(self):
        response = self.client.post(
            reverse("areas:create"),
            {
                "name": "Planchado",
                "description": "Correccion de carroceria",
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("areas:list"))
        self.assertTrue(Area.objects.filter(name="Planchado").exists())

    def test_area_update_view_updates_area(self):
        area = Area.objects.create(name="Mecanica")

        response = self.client.post(
            reverse("areas:edit", args=[area.pk]),
            {
                "name": "Mecanica general",
                "description": "",
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("areas:list"))
        area.refresh_from_db()
        self.assertEqual(area.name, "Mecanica general")
