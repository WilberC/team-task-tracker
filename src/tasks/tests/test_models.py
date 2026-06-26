"""Model tests for the tasks module."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.tasks.models import Task, TaskPriority, TaskStatus
from src.tasks.selectors import subtask_progress
from src.tasks.services import (
    assign_task,
    cancel_task,
    create_subtask,
    create_top_level_task,
    mark_overdue_tasks,
    update_status,
)
from src.teams.models import Team
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrderStatus
from src.workshop.services import generate_job_order


class TaskTestCase(TestCase):
    def setUp(self):
        self.area = Area.objects.create(name="Mecanica")
        self.other_area = Area.objects.create(name="Electricidad")
        self.employee = Employee.objects.create(
            full_name="Carlos Ramos",
            area=self.area,
            position="Mecanico",
        )
        self.team = Team.objects.create(name="Equipo A", area=self.area)
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
            "due_date": timezone.localdate() + timedelta(days=2),
        }
        data.update(overrides)
        return Task.objects.create(**data)


class TaskModelRuleTests(TaskTestCase):
    def test_top_level_task_must_have_job_order(self):
        task = Task(
            title="Diagnostico",
            area=self.area,
            assigned_employee=self.employee,
            due_date=timezone.localdate(),
        )

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_subtask_cannot_have_own_job_order(self):
        parent = self.make_task()
        subtask = Task(
            title="Escaneo",
            parent_task=parent,
            job_order=self.job_order,
            area=self.area,
            assigned_employee=self.employee,
            due_date=timezone.localdate(),
        )

        with self.assertRaises(ValidationError):
            subtask.full_clean()

    def test_subtask_cannot_be_parent(self):
        parent = self.make_task()
        subtask = create_subtask(
            parent,
            title="Escaneo",
            assigned_employee=self.employee,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate(),
        )

        with self.assertRaises(ValidationError):
            create_subtask(
                subtask,
                title="Nivel no permitido",
                assigned_employee=self.employee,
                priority=TaskPriority.MEDIUM,
                due_date=timezone.localdate(),
            )

    def test_task_requires_exactly_one_assignment(self):
        with self.assertRaises(ValidationError):
            self.make_task(assigned_employee=None)

        with self.assertRaises(ValidationError):
            self.make_task(assigned_team=self.team)

    def test_subtask_area_defaults_to_parent_area(self):
        parent = self.make_task(area=self.other_area)

        subtask = create_subtask(
            parent,
            title="Revision de cableado",
            assigned_employee=self.employee,
            priority=TaskPriority.HIGH,
            due_date=timezone.localdate(),
        )

        self.assertEqual(subtask.area, self.other_area)


class TaskServiceTests(TaskTestCase):
    def test_create_top_level_task_starts_pending(self):
        task = create_top_level_task(
            self.job_order,
            title="Diagnostico",
            area=self.area,
            assigned_employee=self.employee,
            priority=TaskPriority.HIGH,
            due_date=timezone.localdate(),
        )

        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_assign_task_sets_one_responsible_party(self):
        task = self.make_task()

        assign_task(task, team=self.team)
        task.refresh_from_db()

        self.assertIsNone(task.assigned_employee)
        self.assertEqual(task.assigned_team, self.team)

    def test_update_status_sets_completion_date(self):
        task = self.make_task()
        update_status(task, TaskStatus.IN_PROGRESS)

        update_status(task, TaskStatus.COMPLETED)
        task.refresh_from_db()

        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.completion_date, timezone.localdate())

    def test_invalid_status_transition_raises_plain_error(self):
        task = self.make_task(status=TaskStatus.COMPLETED)

        with self.assertRaisesMessage(
            ValidationError,
            "Este cambio de estado no esta permitido.",
        ):
            update_status(task, TaskStatus.IN_PROGRESS)

    def test_cancel_task_marks_cancelled(self):
        task = self.make_task()

        cancel_task(task)
        task.refresh_from_db()

        self.assertEqual(task.status, TaskStatus.CANCELLED)

    def test_mark_overdue_tasks_marks_late_open_work(self):
        late = self.make_task(due_date=timezone.localdate() - timedelta(days=1))
        self.make_task(title="A tiempo", due_date=timezone.localdate())

        count = mark_overdue_tasks()
        late.refresh_from_db()

        self.assertEqual(count, 1)
        self.assertEqual(late.status, TaskStatus.OVERDUE)

    def test_parent_completes_when_all_subtasks_done_or_cancelled(self):
        parent = self.make_task()
        first = create_subtask(
            parent,
            title="Escaneo",
            assigned_employee=self.employee,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate(),
        )
        second = create_subtask(
            parent,
            title="Prueba de ruta",
            assigned_employee=self.employee,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate(),
        )

        update_status(first, TaskStatus.IN_PROGRESS)
        update_status(first, TaskStatus.COMPLETED)
        cancel_task(second)
        parent.refresh_from_db()

        self.assertEqual(parent.status, TaskStatus.COMPLETED)
        self.assertEqual(parent.completion_date, timezone.localdate())

    def test_progress_flags_parent_at_risk_when_subtask_overdue(self):
        parent = self.make_task()
        subtask = create_subtask(
            parent,
            title="Escaneo",
            assigned_employee=self.employee,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate() - timedelta(days=1),
        )
        update_status(subtask, TaskStatus.OVERDUE)

        progress = subtask_progress(parent)

        self.assertEqual(progress.total, 1)
        self.assertTrue(progress.at_risk)

    def test_job_order_status_rolls_up_from_tasks(self):
        task = self.make_task()
        self.job_order.refresh_from_db()
        self.assertEqual(self.job_order.status, JobOrderStatus.OPEN)

        update_status(task, TaskStatus.IN_PROGRESS)
        self.job_order.refresh_from_db()
        self.assertEqual(self.job_order.status, JobOrderStatus.IN_PROGRESS)

        update_status(task, TaskStatus.COMPLETED)
        self.job_order.refresh_from_db()
        self.assertEqual(self.job_order.status, JobOrderStatus.DONE)


class TaskViewTests(TaskTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_superuser(
            username="admin",
            password="password",
            email="admin@example.com",
        )
        self.client.force_login(self.user)

    def test_top_level_task_create_view_creates_task(self):
        response = self.client.post(
            reverse("tasks:create", args=[self.job_order.pk]),
            {
                "title": "Diagnostico",
                "description": "Escaneo inicial",
                "area": self.area.pk,
                "assigned_employee": self.employee.pk,
                "assigned_team": "",
                "priority": TaskPriority.HIGH,
                "start_date": "",
                "due_date": timezone.localdate(),
            },
        )

        task = Task.objects.get(title="Diagnostico")
        self.assertRedirects(response, reverse("tasks:detail", args=[task.pk]))

    def test_subtask_create_view_creates_subtask(self):
        parent = self.make_task()

        response = self.client.post(
            reverse("tasks:create_subtask", args=[parent.pk]),
            {
                "title": "Escaneo",
                "description": "",
                "area": "",
                "assigned_employee": self.employee.pk,
                "assigned_team": "",
                "priority": TaskPriority.MEDIUM,
                "start_date": "",
                "due_date": timezone.localdate(),
            },
        )

        subtask = Task.objects.get(title="Escaneo")
        self.assertRedirects(response, reverse("tasks:detail", args=[subtask.pk]))
        self.assertEqual(subtask.parent_task, parent)

    def test_task_detail_renders_assignment_status_and_dates(self):
        task = self.make_task()

        response = self.client.get(reverse("tasks:detail", args=[task.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carlos Ramos")
        self.assertContains(response, "Pendiente")

    def test_task_list_filters_by_status(self):
        self.make_task(title="Pendiente")
        self.make_task(title="Vencida", status=TaskStatus.OVERDUE)

        response = self.client.get(
            reverse("tasks:list"), {"status": TaskStatus.OVERDUE}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vencida")
        self.assertNotContains(response, "<strong>Pendiente</strong>", html=True)

    def test_kanban_board_groups_tasks_by_status(self):
        self.make_task(title="Tarea pendiente")
        self.make_task(title="Tarea vencida", status=TaskStatus.OVERDUE)

        response = self.client.get(reverse("tasks:kanban"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pendiente")
        self.assertContains(response, "Vencida")
        self.assertContains(response, "Tarea pendiente")
        self.assertContains(response, "Tarea vencida")

    def test_htmx_task_list_filters_without_full_page(self):
        self.make_task(title="Pendiente")
        self.make_task(title="Vencida", status=TaskStatus.OVERDUE)

        response = self.client.get(
            reverse("tasks:list"),
            {"status": TaskStatus.OVERDUE},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="task-results"')
        self.assertContains(response, "Vencida")
        self.assertNotContains(response, "site-shell")
        self.assertNotContains(response, "<strong>Pendiente</strong>", html=True)

    def test_status_update_json_persists(self):
        task = self.make_task()

        response = self.client.post(
            reverse("tasks:status", args=[task.pk]),
            {"status": TaskStatus.IN_PROGRESS},
            HTTP_ACCEPT="application/json",
        )

        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], TaskStatus.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

    def test_invalid_kanban_drop_returns_rollback_status(self):
        task = self.make_task()

        response = self.client.post(
            reverse("tasks:status", args=[task.pk]),
            {"status": TaskStatus.COMPLETED, "response": "card"},
            HTTP_HX_REQUEST="true",
            HTTP_X_KANBAN_DROP="true",
        )

        task.refresh_from_db()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_subtask_create_htmx_refreshes_parent_section(self):
        parent = self.make_task()

        response = self.client.post(
            reverse("tasks:create_subtask", args=[parent.pk]),
            {
                "title": "Escaneo",
                "description": "",
                "area": "",
                "assigned_employee": self.employee.pk,
                "assigned_team": "",
                "priority": TaskPriority.MEDIUM,
                "start_date": "",
                "due_date": timezone.localdate(),
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(parent.subtasks.filter(title="Escaneo").exists())
        self.assertContains(response, 'id="subtask-section"')
        self.assertContains(response, "Escaneo")

    def test_subtask_inline_edit_htmx_updates_row(self):
        parent = self.make_task()
        subtask = create_subtask(
            parent,
            title="Escaneo",
            assigned_employee=self.employee,
            priority=TaskPriority.MEDIUM,
            due_date=timezone.localdate(),
        )

        response = self.client.post(
            reverse("tasks:edit", args=[subtask.pk]),
            {
                "title": "Escaneo completo",
                "description": "",
                "area": "",
                "assigned_employee": self.employee.pk,
                "assigned_team": "",
                "priority": TaskPriority.HIGH,
                "start_date": "",
                "due_date": timezone.localdate(),
            },
            HTTP_HX_REQUEST="true",
        )

        subtask.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(subtask.title, "Escaneo completo")
        self.assertContains(response, 'id="subtask-row-')
        self.assertContains(response, "Escaneo completo")
