"""Views for the tasks module."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView, UpdateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import (
    ADMINISTRATOR,
    MECHANIC,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
    can_cancel_task,
    can_create_subtask,
    can_edit_task,
    can_update_task_status,
    can_view_task,
    task_queryset_for_user,
)
from src.tasks.forms import TaskFilterForm, TaskForm
from src.tasks.models import Task, TaskStatus
from src.tasks.selectors import (
    kanban_columns,
    subtask_progress,
    task_with_subtasks,
    tasks_list,
)
from src.tasks.services import (
    cancel_task,
    create_subtask,
    create_top_level_task,
    update_status,
)
from src.workshop.models import JobOrder


def _is_htmx(request) -> bool:
    return request.headers.get("HX-Request") == "true"


def _task_filters(form: TaskFilterForm) -> dict:
    if not form.is_valid():
        return {}
    return {
        key: value.pk if hasattr(value, "pk") else value
        for key, value in form.cleaned_data.items()
        if value
    }


def _plain_validation_message(error: ValidationError) -> str:
    if hasattr(error, "messages") and error.messages:
        return error.messages[0]
    return "No se pudo guardar el cambio. Revise los datos e intente nuevamente."


def _subtask_section_context(parent_task: Task, subtask_form=None) -> dict:
    parent_task = task_with_subtasks(parent_task.pk)
    return {
        "task": parent_task,
        "progress": subtask_progress(parent_task),
        "status_choices": TaskStatus.choices,
        "subtask_form": subtask_form or TaskForm(parent_task=parent_task),
    }


def _kanban_column_context(filters: dict) -> list[dict]:
    columns = kanban_columns(filters)
    return [
        {
            "status": status,
            "label": label,
            "tasks": columns[status],
        }
        for status, label in TaskStatus.choices
    ]


class TaskListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        MECHANIC,
        REPORTS_VIEWER,
    )
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        self.filter_form = TaskFilterForm(self.request.GET or None)
        allowed_ids = task_queryset_for_user(self.request.user).values("pk")
        return tasks_list(_task_filters(self.filter_form)).filter(pk__in=allowed_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context

    def get_template_names(self):
        if _is_htmx(self.request):
            return ["tasks/partials/task_table.html"]
        return [self.template_name]


class TaskKanbanView(RoleRequiredMixin, View):
    allowed_roles = (
        ADMINISTRATOR,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        MECHANIC,
        REPORTS_VIEWER,
    )

    def get(self, request):
        filter_form = TaskFilterForm(request.GET or None)
        allowed_ids = task_queryset_for_user(request.user).values("pk")
        filters = _task_filters(filter_form)
        columns = kanban_columns(filters)
        restricted_columns = {
            status: queryset.filter(pk__in=allowed_ids)
            for status, queryset in columns.items()
        }
        context = {
            "filter_form": filter_form,
            "columns": [
                {"status": status, "label": label, "tasks": restricted_columns[status]}
                for status, label in TaskStatus.choices
            ],
            "status_choices": TaskStatus.choices,
        }
        template_name = (
            "tasks/partials/kanban_board.html"
            if _is_htmx(request)
            else "tasks/kanban.html"
        )
        return render(request, template_name, context)


class TaskDetailView(RoleRequiredMixin, DetailView):
    allowed_roles = (
        ADMINISTRATOR,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        MECHANIC,
        REPORTS_VIEWER,
    )
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        task = task_with_subtasks(self.kwargs["pk"])
        if not can_view_task(self.request.user, task):
            raise PermissionDenied("No tiene permiso para usar esta tarea.")
        return task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress"] = subtask_progress(self.object)
        context["status_choices"] = TaskStatus.choices
        if self.object.is_top_level:
            context["subtask_form"] = TaskForm(parent_task=self.object)
        return context


class TopLevelTaskCreateView(RoleRequiredMixin, FormView):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR)
    template_name = "tasks/task_form.html"
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        self.job_order = get_object_or_404(JobOrder, pk=kwargs["job_order_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["job_order"] = self.job_order
        return kwargs

    def form_valid(self, form):
        task = create_top_level_task(self.job_order, **form.cleaned_data)
        messages.success(self.request, "Tarea registrada.")
        return redirect("tasks:detail", pk=task.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Agregar tarea"
        context["submit_label"] = "Guardar tarea"
        context["cancel_url"] = reverse("workshop:detail", args=[self.job_order.pk])
        return context


class SubtaskCreateView(RoleRequiredMixin, FormView):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR, MECHANIC)
    template_name = "tasks/task_form.html"
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.parent_task = get_object_or_404(Task, pk=kwargs["parent_pk"])
        if not can_create_subtask(request.user, self.parent_task):
            raise PermissionDenied("No tiene permiso para agregar subtareas aqui.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["parent_task"] = self.parent_task
        return kwargs

    def form_valid(self, form):
        task = create_subtask(self.parent_task, **form.cleaned_data)
        if _is_htmx(self.request):
            return render(
                self.request,
                "tasks/partials/subtask_section.html",
                _subtask_section_context(task.parent_task),
            )
        messages.success(self.request, "Subtarea registrada.")
        return redirect("tasks:detail", pk=task.pk)

    def form_invalid(self, form):
        if _is_htmx(self.request):
            return render(
                self.request,
                "tasks/partials/subtask_section.html",
                _subtask_section_context(self.parent_task, form),
                status=422,
            )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Agregar subtarea"
        context["submit_label"] = "Guardar subtarea"
        context["cancel_url"] = reverse("tasks:detail", args=[self.parent_task.pk])
        return context


class TaskUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR, MECHANIC)
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    context_object_name = "task"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task = self.object
        if task.parent_task_id:
            kwargs["parent_task"] = task.parent_task
        else:
            kwargs["job_order"] = task.job_order
        return kwargs

    def get_object(self, queryset=None):
        task = super().get_object(queryset)
        if not can_edit_task(self.request.user, task):
            raise PermissionDenied("No tiene permiso para editar esta tarea.")
        return task

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if _is_htmx(request) and self.object.parent_task_id:
            return render(
                request,
                "tasks/partials/subtask_row_form.html",
                {
                    "task": self.object.parent_task,
                    "subtask": self.object,
                    "form": self.get_form(),
                },
            )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        if _is_htmx(self.request) and self.object.parent_task_id:
            return render(
                self.request,
                "tasks/partials/subtask_row.html",
                {
                    "task": self.object.parent_task,
                    "subtask": self.object,
                    "status_choices": TaskStatus.choices,
                },
            )
        messages.success(self.request, "Tarea actualizada.")
        return redirect("tasks:detail", pk=self.object.pk)

    def form_invalid(self, form):
        if _is_htmx(self.request) and self.object.parent_task_id:
            return render(
                self.request,
                "tasks/partials/subtask_row_form.html",
                {
                    "task": self.object.parent_task,
                    "subtask": self.object,
                    "form": form,
                },
                status=422,
            )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar tarea"
        context["submit_label"] = "Guardar cambios"
        context["cancel_url"] = reverse("tasks:detail", args=[self.object.pk])
        return context


class TaskStatusUpdateView(RoleRequiredMixin, View):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR, MECHANIC)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if not can_update_task_status(request.user, task):
            raise PermissionDenied("No tiene permiso para actualizar esta tarea.")
        new_status = request.POST.get("status")
        try:
            task = update_status(task, new_status)
        except ValidationError as error:
            message = _plain_validation_message(error)
            if request.headers.get("Accept") == "application/json":
                return JsonResponse({"ok": False, "error": message}, status=422)
            if _is_htmx(request):
                if request.POST.get("response") == "card":
                    if request.headers.get("X-Kanban-Drop") == "true":
                        return render(
                            request,
                            "tasks/partials/kanban_card.html",
                            {
                                "task": task,
                                "status_choices": TaskStatus.choices,
                                "card_error": message,
                            },
                            status=422,
                        )
                    return render(
                        request,
                        "tasks/partials/kanban_card.html",
                        {
                            "task": task,
                            "status_choices": TaskStatus.choices,
                            "card_error": message,
                        },
                    )
                return render(
                    request,
                    "tasks/partials/task_status_panel.html",
                    {
                        "task": task,
                        "status_choices": TaskStatus.choices,
                        "status_error": message,
                    },
                    status=422,
                )
            messages.error(request, message)
            return redirect("tasks:detail", pk=task.pk)

        if request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {
                    "ok": True,
                    "id": task.pk,
                    "status": task.status,
                    "status_label": task.get_status_display(),
                }
            )
        if _is_htmx(request):
            if request.POST.get("response") == "card":
                return render(
                    request,
                    "tasks/partials/kanban_card.html",
                    {"task": task, "status_choices": TaskStatus.choices},
                )
            return render(
                request,
                "tasks/partials/task_status_panel.html",
                {"task": task, "status_choices": TaskStatus.choices},
            )
        messages.success(request, "Estado actualizado.")
        return redirect("tasks:detail", pk=task.pk)


class TaskCancelView(RoleRequiredMixin, View):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if not can_cancel_task(request.user, task):
            raise PermissionDenied("No tiene permiso para cancelar esta tarea.")
        cancel_task(task)
        messages.success(request, "Tarea cancelada.")
        return redirect("tasks:detail", pk=task.pk)
