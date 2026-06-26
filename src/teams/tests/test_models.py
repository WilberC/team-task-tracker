"""Model tests for the teams module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.areas.models import Area
from src.employees.models import Employee
from src.teams.models import Team
from src.teams.selectors import active_teams_by_area


class TeamModelTests(TestCase):
    def test_team_string_uses_name(self):
        area = Area.objects.create(name="Mecanica")
        team = Team.objects.create(name="Equipo A", area=area)

        self.assertEqual(str(team), "Equipo A")

    def test_active_teams_by_area_excludes_inactive_teams_and_areas(self):
        area = Area.objects.create(name="Mecanica")
        inactive_area = Area.objects.create(name="Pintura", active=False)
        active_team = Team.objects.create(name="Equipo A", area=area)
        Team.objects.create(name="Equipo B", area=area, active=False)
        Team.objects.create(name="Equipo C", area=inactive_area)

        self.assertQuerySetEqual(active_teams_by_area(area.pk), [active_team])


class TeamViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.area = Area.objects.create(name="Mecanica")
        self.employee = Employee.objects.create(
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )

    def test_team_list_renders_registered_teams(self):
        team = Team.objects.create(name="Equipo rapido", area=self.area)
        team.members.add(self.employee)

        response = self.client.get(reverse("teams:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Equipo rapido")
        self.assertContains(response, "Carlos Ramos")

    def test_team_create_view_creates_team(self):
        response = self.client.post(
            reverse("teams:create"),
            {
                "name": "Equipo mecanica",
                "area": self.area.pk,
                "members": [self.employee.pk],
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("teams:list"))
        team = Team.objects.get(name="Equipo mecanica")
        self.assertQuerySetEqual(team.members.all(), [self.employee])

    def test_team_update_view_updates_team(self):
        team = Team.objects.create(name="Equipo A", area=self.area)

        response = self.client.post(
            reverse("teams:edit", args=[team.pk]),
            {
                "name": "Equipo senior",
                "area": self.area.pk,
                "members": [self.employee.pk],
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("teams:list"))
        team.refresh_from_db()
        self.assertEqual(team.name, "Equipo senior")
        self.assertQuerySetEqual(team.members.all(), [self.employee])
