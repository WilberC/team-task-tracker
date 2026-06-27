"""Tests for report selector aggregations."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.reports.selectors import (
    deadline_compliance,
    overdue_tasks,
    productivity_by_area,
    tasks_by_status,
    workload_by_assignee,
)
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.tasks.models import Task, TaskPriority, TaskStatus
from src.teams.models import Team
from src.vehicles.models import Vehicle
from src.workshop.services import generate_job_order


class ReportSelectorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)
        self.today = timezone.localdate()
        self.area = Area.objects.create(name="Mecanica")
        self.paint_area = Area.objects.create(name="Pintura")
        self.employee = Employee.objects.create(
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )
        self.team = Team.objects.create(name="Equipo Pintura", area=self.paint_area)
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

    def make_task(self, **overrides):
        data = {
            "job_order": self.job_order,
            "title": "Diagnostico",
            "area": self.area,
            "assigned_employee": self.employee,
            "priority": TaskPriority.MEDIUM,
            "status": TaskStatus.PENDING,
            "due_date": self.today,
        }
        data.update(overrides)
        return Task.objects.create(**data)

    def test_tasks_by_status_counts_all_statuses(self):
        self.make_task(title="Pendiente")
        self.make_task(title="Vencida", status=TaskStatus.OVERDUE)

        counts = {item.status: item.count for item in tasks_by_status()}

        self.assertEqual(counts[TaskStatus.PENDING], 1)
        self.assertEqual(counts[TaskStatus.OVERDUE], 1)
        self.assertEqual(counts[TaskStatus.COMPLETED], 0)

    def test_overdue_tasks_returns_open_late_work_only(self):
        late = self.make_task(due_date=self.today - timedelta(days=1))
        self.make_task(
            title="Cerrada tarde",
            status=TaskStatus.COMPLETED,
            due_date=self.today - timedelta(days=2),
            completion_date=self.today,
        )

        result = list(overdue_tasks(self.today))

        self.assertEqual(result, [late])

    def test_workload_by_assignee_counts_employee_and_team_open_tasks(self):
        self.make_task(title="Empleado")
        self.make_task(
            title="Equipo",
            area=self.paint_area,
            assigned_employee=None,
            assigned_team=self.team,
        )
        self.make_task(
            title="Cerrada",
            status=TaskStatus.COMPLETED,
            completion_date=self.today,
        )

        workload = {
            (item.kind, item.assignee): item.count for item in workload_by_assignee()
        }

        self.assertEqual(workload[("Empleado", "Carlos Ramos")], 1)
        self.assertEqual(workload[("Equipo", "Equipo Pintura")], 1)

    def test_productivity_by_area_counts_completed_tasks_in_range(self):
        self.make_task(
            title="Mecanica completa",
            status=TaskStatus.COMPLETED,
            completion_date=self.today,
        )
        self.make_task(
            title="Pintura completa",
            area=self.paint_area,
            assigned_employee=None,
            assigned_team=self.team,
            status=TaskStatus.COMPLETED,
            completion_date=self.today,
        )
        self.make_task(
            title="Fuera de rango",
            status=TaskStatus.COMPLETED,
            completion_date=self.today - timedelta(days=40),
        )

        productivity = {
            item.area: item.completed
            for item in productivity_by_area(
                self.today - timedelta(days=7),
                self.today,
            )
        }

        self.assertEqual(productivity["Mecanica"], 1)
        self.assertEqual(productivity["Pintura"], 1)

    def test_deadline_compliance_calculates_on_time_and_late_percentages(self):
        self.make_task(
            title="A tiempo",
            status=TaskStatus.COMPLETED,
            due_date=self.today,
            completion_date=self.today,
        )
        self.make_task(
            title="Tarde",
            status=TaskStatus.COMPLETED,
            due_date=self.today - timedelta(days=1),
            completion_date=self.today,
        )

        compliance = deadline_compliance(self.today - timedelta(days=7), self.today)

        self.assertEqual(compliance.on_time_count, 1)
        self.assertEqual(compliance.late_count, 1)
        self.assertEqual(compliance.on_time_percent, 50)
        self.assertEqual(compliance.late_percent, 50)

    def test_reports_page_renders_all_five_reports(self):
        response = self.client.get(reverse("reports:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1. Tareas por estado")
        self.assertContains(response, "5. Cumplimiento de fechas")

    def test_reports_page_applies_selected_date_range_to_all_reports(self):
        start_date = self.today - timedelta(days=2)
        end_date = self.today - timedelta(days=1)
        self.make_task(title="Dentro abierta", due_date=end_date)
        self.make_task(title="Fuera abierta", due_date=self.today + timedelta(days=5))
        self.make_task(title="Fuera vencida", due_date=self.today - timedelta(days=3))
        self.make_task(
            title="Dentro completada",
            status=TaskStatus.COMPLETED,
            due_date=start_date,
            completion_date=end_date,
        )
        self.make_task(
            title="Fuera completada",
            status=TaskStatus.COMPLETED,
            due_date=self.today - timedelta(days=3),
            completion_date=self.today - timedelta(days=3),
        )

        response = self.client.get(
            reverse("reports:index"),
            {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )

        status_counts = {
            item.status: item.count for item in response.context["status_counts"]
        }
        overdue_titles = [task.title for task in response.context["overdue_tasks"]]
        workload = {
            (item.kind, item.assignee): item.count
            for item in response.context["workload"]
        }
        productivity = {
            item.area: item.completed for item in response.context["productivity"]
        }
        deadline = response.context["deadline"]

        self.assertEqual(status_counts[TaskStatus.PENDING], 1)
        self.assertEqual(status_counts[TaskStatus.COMPLETED], 1)
        self.assertEqual(overdue_titles, ["Dentro abierta"])
        self.assertEqual(workload[("Empleado", "Carlos Ramos")], 1)
        self.assertEqual(productivity["Mecanica"], 1)
        self.assertEqual(deadline.on_time_count, 0)
        self.assertEqual(deadline.late_count, 1)
