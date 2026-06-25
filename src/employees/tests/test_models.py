"""Model tests for the employees module."""

from django.test import TestCase
from django.urls import reverse

from src.areas.models import Area
from src.employees.models import Employee
from src.employees.selectors import active_employees_by_area


class EmployeeModelTests(TestCase):
    def test_employee_string_uses_full_name(self):
        area = Area.objects.create(name="Mecanica")
        employee = Employee.objects.create(
            full_name="Carlos Ramos",
            email="carlos@example.com",
            area=area,
            position="Mecanico",
        )

        self.assertEqual(str(employee), "Carlos Ramos")

    def test_active_employees_by_area_excludes_inactive_people_and_areas(self):
        area = Area.objects.create(name="Electricidad")
        inactive_area = Area.objects.create(name="Pintura", active=False)
        active_employee = Employee.objects.create(
            full_name="Ana Torres",
            area=area,
            position="Tecnica electrica",
        )
        Employee.objects.create(
            full_name="Luis Inactivo",
            area=area,
            position="Mecanico",
            active=False,
        )
        Employee.objects.create(
            full_name="Empleado en area inactiva",
            area=inactive_area,
            position="Pintor",
        )

        self.assertQuerySetEqual(
            active_employees_by_area(area.pk),
            [active_employee],
        )


class EmployeeViewTests(TestCase):
    def setUp(self):
        self.area = Area.objects.create(name="Mecanica")

    def test_employee_list_renders_registered_employees(self):
        Employee.objects.create(
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )

        response = self.client.get(reverse("employees:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carlos Ramos")

    def test_employee_create_view_creates_employee(self):
        response = self.client.post(
            reverse("employees:create"),
            {
                "full_name": "Maria Lopez",
                "email": "maria@example.com",
                "area": self.area.pk,
                "position": "Asesora",
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("employees:list"))
        self.assertTrue(Employee.objects.filter(full_name="Maria Lopez").exists())

    def test_employee_update_view_updates_employee(self):
        employee = Employee.objects.create(
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )

        response = self.client.post(
            reverse("employees:edit", args=[employee.pk]),
            {
                "full_name": "Carlos A. Ramos",
                "email": "",
                "area": self.area.pk,
                "position": "Tecnico mecanico",
                "active": "on",
            },
        )

        self.assertRedirects(response, reverse("employees:list"))
        employee.refresh_from_db()
        self.assertEqual(employee.full_name, "Carlos A. Ramos")
