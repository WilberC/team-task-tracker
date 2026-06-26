"""Views for read-only reports."""

from datetime import timedelta

from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import ADMINISTRATOR, REPORTS_VIEWER, WORKSHOP_SUPERVISOR
from src.reports.selectors import (
    deadline_compliance,
    overdue_tasks,
    productivity_by_area,
    tasks_by_status,
    workload_by_assignee,
)


class ReportsView(RoleRequiredMixin, TemplateView):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR, REPORTS_VIEWER)
    template_name = "reports/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        end_date = _date_from_query(self.request.GET.get("end_date"))
        end_date = end_date or timezone.localdate()
        start_date = _date_from_query(self.request.GET.get("start_date"))
        start_date = start_date or end_date - timedelta(days=30)
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        context.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "status_counts": tasks_by_status(),
                "overdue_tasks": overdue_tasks(),
                "workload": workload_by_assignee(),
                "productivity": productivity_by_area(start_date, end_date),
                "deadline": deadline_compliance(start_date, end_date),
            }
        )
        return context


def _date_from_query(value: str | None):
    return parse_date(value) if value else None
