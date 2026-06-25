"""Views for the sales module."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from src.sales.forms import ServiceOrderForm
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.sales.selectors import service_orders_list
from src.workshop.services import generate_job_order


class ServiceOrderListView(ListView):
    model = ServiceOrder
    template_name = "sales/serviceorder_list.html"
    context_object_name = "service_orders"

    def get_queryset(self):
        return service_orders_list()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["open_count"] = ServiceOrder.objects.filter(
            status=ServiceOrderStatus.OPEN
        ).count()
        context["approved_count"] = ServiceOrder.objects.filter(
            status=ServiceOrderStatus.APPROVED
        ).count()
        context["closed_count"] = ServiceOrder.objects.filter(
            status=ServiceOrderStatus.CLOSED
        ).count()
        return context


class ServiceOrderCreateView(CreateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = "sales/serviceorder_form.html"
    success_url = reverse_lazy("sales:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Registrar orden de servicio"
        context["submit_label"] = "Guardar orden"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.status == ServiceOrderStatus.APPROVED:
            generate_job_order(self.object)
        return response


class ServiceOrderUpdateView(UpdateView):
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = "sales/serviceorder_form.html"
    success_url = reverse_lazy("sales:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Editar orden de servicio"
        context["submit_label"] = "Guardar cambios"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.status == ServiceOrderStatus.APPROVED:
            generate_job_order(self.object)
        return response


class ServiceOrderApproveView(View):
    def post(self, request, pk):
        service_order = get_object_or_404(ServiceOrder, pk=pk)
        job_order = generate_job_order(service_order)
        messages.success(
            request,
            f"Orden aprobada. Se genero la orden de trabajo OT-{job_order.pk}.",
        )
        return redirect("workshop:detail", pk=job_order.pk)
