"""Views for the tasks module."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView

from src.tasks.forms import TaskFilterForm, TaskForm
from src.tasks.models import Task, TaskStatus
from src.tasks.selectors import subtask_progress, task_with_subtasks, tasks_list
from src.tasks.services import (
    cancel_task,
    create_subtask,
    create_top_level_task,
    update_status,
)
from src.workshop.models import JobOrder


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        self.filter_form = TaskFilterForm(self.request.GET or None)
        filters = {}
        if self.filter_form.is_valid():
            filters = {
                key: value.pk if hasattr(value, "pk") else value
                for key, value in self.filter_form.cleaned_data.items()
                if value
            }
        return tasks_list(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        return task_with_subtasks(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress"] = subtask_progress(self.object)
        context["status_choices"] = TaskStatus.choices
        return context


class TopLevelTaskCreateView(FormView):
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


class SubtaskCreateView(FormView):
    template_name = "tasks/task_form.html"
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        self.parent_task = get_object_or_404(Task, pk=kwargs["parent_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["parent_task"] = self.parent_task
        return kwargs

    def form_valid(self, form):
        task = create_subtask(self.parent_task, **form.cleaned_data)
        messages.success(self.request, "Subtarea registrada.")
        return redirect("tasks:detail", pk=task.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Agregar subtarea"
        context["submit_label"] = "Guardar subtarea"
        context["cancel_url"] = reverse("tasks:detail", args=[self.parent_task.pk])
        return context


class TaskStatusUpdateView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get("status")
        update_status(task, new_status)
        messages.success(request, "Estado actualizado.")
        return redirect("tasks:detail", pk=task.pk)


class TaskCancelView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        cancel_task(task)
        messages.success(request, "Tarea cancelada.")
        return redirect("tasks:detail", pk=task.pk)
