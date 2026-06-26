"""Views for the clients module."""

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
from src.clients.forms import ClientForm
from src.clients.models import Client


class ClientListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    )
    model = Client
    template_name = "clients/client_list.html"
    context_object_name = "clients"


class ClientCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = (ADMINISTRATOR, FRONT_DESK, SERVICE_ADVISOR)
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar cliente"
        context["submit_label"] = "Guardar cliente"
        return context


class ClientUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = (ADMINISTRATOR, FRONT_DESK, SERVICE_ADVISOR)
    model = Client
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar cliente"
        context["submit_label"] = "Guardar cambios"
        return context
