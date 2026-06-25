"""Views for the operational dashboard."""

from django.shortcuts import render
from django.views.generic import TemplateView

from src.dashboard.selectors import current_area_load, dashboard_snapshot


class DashboardView(TemplateView):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get("HX-Request") == "true":
            return render(request, "dashboard/partials/counters.html", context)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["snapshot"] = dashboard_snapshot()
        context["area_load"] = current_area_load()
        return context
