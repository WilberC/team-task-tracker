"""Views for the employees module."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import (
    ADMINISTRATOR,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
)
from src.employees.forms import EmployeeForm
from src.employees.models import Employee


class EmployeeListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    )
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"

    def get_queryset(self):
        return Employee.objects.select_related("area").order_by("full_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_count"] = Employee.objects.filter(
            active=True,
            area__active=True,
        ).count()
        context["inactive_count"] = Employee.objects.exclude(
            active=True,
            area__active=True,
        ).count()
        return context


class EmployeeCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = (ADMINISTRATOR,)
    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"
    success_url = reverse_lazy("employees:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar empleado"
        context["submit_label"] = "Guardar empleado"
        return context


class EmployeeUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = (ADMINISTRATOR,)
    model = Employee
    form_class = EmployeeForm
    template_name = "employees/employee_form.html"
    success_url = reverse_lazy("employees:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar empleado"
        context["submit_label"] = "Guardar cambios"
        return context
