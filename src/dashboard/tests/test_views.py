"""Tests for dashboard views."""

from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_dashboard_page_renders_summary_sections(self):
        response = self.client.get(reverse("dashboard:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vehiculos en taller")
        self.assertContains(response, "Responsables activos")

    def test_dashboard_htmx_request_returns_counters_partial(self):
        response = self.client.get(reverse("dashboard:index"), HTTP_HX_REQUEST="true")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="dashboard-counters"')
        self.assertNotContains(response, "site-shell")
