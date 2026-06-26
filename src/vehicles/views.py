"""Views for the vehicles module."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import (
    ADMINISTRATOR,
    FRONT_DESK,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
)
from src.vehicles.forms import VehicleForm
from src.vehicles.models import Vehicle
from src.vehicles.selectors import vehicles_list


class VehicleListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    )
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        return vehicles_list()


class VehicleCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = (ADMINISTRATOR, FRONT_DESK, SERVICE_ADVISOR)
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar vehiculo"
        context["submit_label"] = "Guardar vehiculo"
        return context


class VehicleUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = (ADMINISTRATOR, FRONT_DESK, SERVICE_ADVISOR)
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar vehiculo"
        context["submit_label"] = "Guardar cambios"
        return context
