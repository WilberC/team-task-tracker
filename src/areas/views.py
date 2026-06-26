"""Views for the areas module."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import (
    ADMINISTRATOR,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
)
from src.areas.forms import AreaForm
from src.areas.models import Area


class AreaListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    )
    model = Area
    template_name = "areas/area_list.html"
    context_object_name = "areas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_count"] = Area.objects.filter(active=True).count()
        context["inactive_count"] = Area.objects.filter(active=False).count()
        return context


class AreaCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = (ADMINISTRATOR,)
    model = Area
    form_class = AreaForm
    template_name = "areas/area_form.html"
    success_url = reverse_lazy("areas:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar area"
        context["submit_label"] = "Guardar area"
        return context


class AreaUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = (ADMINISTRATOR,)
    model = Area
    form_class = AreaForm
    template_name = "areas/area_form.html"
    success_url = reverse_lazy("areas:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar area"
        context["submit_label"] = "Guardar cambios"
        return context
