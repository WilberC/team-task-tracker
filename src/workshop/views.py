"""Views for the workshop module."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from src.workshop.models import JobOrder
from src.workshop.selectors import job_order_with_tasks, open_job_orders
from src.workshop.services import close_job_order, mark_job_order_delivered


class JobOrderListView(ListView):
    model = JobOrder
    template_name = "workshop/joborder_list.html"
    context_object_name = "job_orders"

    def get_queryset(self):
        return open_job_orders()


class JobOrderDetailView(DetailView):
    model = JobOrder
    template_name = "workshop/joborder_detail.html"
    context_object_name = "job_order"

    def get_object(self, queryset=None):
        return job_order_with_tasks(self.kwargs["pk"])


class JobOrderCloseView(View):
    def post(self, request, pk):
        job_order = get_object_or_404(JobOrder, pk=pk)
        close_job_order(job_order)
        messages.success(request, "Orden de trabajo cerrada.")
        return redirect("workshop:detail", pk=job_order.pk)


class JobOrderDeliverView(View):
    def post(self, request, pk):
        job_order = get_object_or_404(JobOrder, pk=pk)
        mark_job_order_delivered(job_order)
        messages.success(request, "Vehiculo marcado como entregado.")
        return redirect("workshop:list")
