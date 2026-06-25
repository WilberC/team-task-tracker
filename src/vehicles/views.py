"""Views for the vehicles module."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from src.vehicles.forms import VehicleForm
from src.vehicles.models import Vehicle
from src.vehicles.selectors import vehicles_list


class VehicleListView(ListView):
    model = Vehicle
    template_name = "vehicles/vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        return vehicles_list()


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar vehiculo"
        context["submit_label"] = "Guardar vehiculo"
        return context


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicles/vehicle_form.html"
    success_url = reverse_lazy("vehicles:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar vehiculo"
        context["submit_label"] = "Guardar cambios"
        return context
