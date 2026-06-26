"""Views for the teams module."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import (
    ADMINISTRATOR,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
)
from src.teams.forms import TeamForm
from src.teams.models import Team


class TeamListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        REPORTS_VIEWER,
    )
    model = Team
    template_name = "teams/team_list.html"
    context_object_name = "teams"

    def get_queryset(self):
        return (
            Team.objects.select_related("area")
            .prefetch_related("members")
            .order_by("name")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_count"] = Team.objects.filter(
            active=True,
            area__active=True,
        ).count()
        context["inactive_count"] = Team.objects.exclude(
            active=True,
            area__active=True,
        ).count()
        return context


class TeamCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = (ADMINISTRATOR,)
    model = Team
    form_class = TeamForm
    template_name = "teams/team_form.html"
    success_url = reverse_lazy("teams:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar equipo"
        context["submit_label"] = "Guardar equipo"
        return context


class TeamUpdateView(RoleRequiredMixin, UpdateView):
    allowed_roles = (ADMINISTRATOR,)
    model = Team
    form_class = TeamForm
    template_name = "teams/team_form.html"
    success_url = reverse_lazy("teams:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar equipo"
        context["submit_label"] = "Guardar cambios"
        return context
