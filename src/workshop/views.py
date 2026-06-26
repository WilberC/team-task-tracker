"""Views for the workshop module."""

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from src.access.mixins import JobOrderObjectAccessMixin, RoleRequiredMixin
from src.access.roles import (
    ADMINISTRATOR,
    FRONT_DESK,
    MECHANIC,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
    job_order_queryset_for_user,
)
from src.workshop.models import JobOrder
from src.workshop.selectors import (
    client_safe_job_order_status,
    job_order_with_tasks,
    open_job_orders,
)
from src.workshop.services import close_job_order, mark_job_order_delivered


class JobOrderListView(RoleRequiredMixin, ListView):
    allowed_roles = (
        ADMINISTRATOR,
        FRONT_DESK,
        SERVICE_ADVISOR,
        WORKSHOP_SUPERVISOR,
        MECHANIC,
        REPORTS_VIEWER,
    )
    model = JobOrder
    template_name = "workshop/joborder_list.html"
    context_object_name = "job_orders"

    def get_queryset(self):
        allowed_ids = job_order_queryset_for_user(self.request.user).values("pk")
        return open_job_orders().filter(pk__in=allowed_ids)


class JobOrderDetailView(JobOrderObjectAccessMixin, DetailView):
    model = JobOrder
    template_name = "workshop/joborder_detail.html"
    context_object_name = "job_order"

    def get_object(self, queryset=None):
        return job_order_with_tasks(self.kwargs["pk"])


class ClientStatusView(TemplateView):
    template_name = "workshop/client_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["status_view"] = client_safe_job_order_status(kwargs["token"])
        except JobOrder.DoesNotExist as error:
            raise Http404("No encontramos el estado solicitado.") from error
        return context


class JobOrderCloseView(RoleRequiredMixin, View):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR)

    def post(self, request, pk):
        job_order = get_object_or_404(JobOrder, pk=pk)
        close_job_order(job_order)
        messages.success(request, "Orden de trabajo cerrada.")
        return redirect("workshop:detail", pk=job_order.pk)


class JobOrderDeliverView(RoleRequiredMixin, View):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR)

    def post(self, request, pk):
        job_order = get_object_or_404(JobOrder, pk=pk)
        mark_job_order_delivered(job_order)
        messages.success(request, "Vehiculo marcado como entregado.")
        return redirect("workshop:list")
