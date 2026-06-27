"""Views for read-only reports."""

from dataclasses import dataclass
from datetime import date, timedelta

from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView

from src.access.mixins import RoleRequiredMixin
from src.access.roles import ADMINISTRATOR, REPORTS_VIEWER, WORKSHOP_SUPERVISOR
from src.reports.exports import build_reports_workbook
from src.reports.selectors import (
    AreaProductivity,
    DeadlineCompliance,
    StatusCount,
    WorkloadCount,
    deadline_compliance,
    overdue_tasks,
    productivity_by_area,
    tasks_by_status,
    tasks_due_between,
    workload_by_assignee,
)
from src.tasks.models import Task


@dataclass(frozen=True)
class ReportsData:
    start_date: date
    end_date: date
    due_date_tasks: tuple[Task, ...]
    status_counts: tuple[StatusCount, ...]
    overdue_tasks: tuple[Task, ...]
    workload: tuple[WorkloadCount, ...]
    productivity: tuple[AreaProductivity, ...]
    deadline: DeadlineCompliance


class ReportsView(RoleRequiredMixin, TemplateView):
    allowed_roles = (ADMINISTRATOR, WORKSHOP_SUPERVISOR, REPORTS_VIEWER)
    template_name = "reports/index.html"

    def get(self, request, *args, **kwargs):
        reports = _reports_data_from_query(request.GET)
        if request.GET.get("export") == "xlsx":
            return _xlsx_response(reports)
        context = self.get_context_data(reports=reports)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = kwargs["reports"]

        context.update(
            {
                "start_date": reports.start_date,
                "end_date": reports.end_date,
                "status_counts": reports.status_counts,
                "overdue_tasks": reports.overdue_tasks,
                "workload": reports.workload,
                "productivity": reports.productivity,
                "deadline": reports.deadline,
                "export_query": (
                    f"start_date={reports.start_date:%Y-%m-%d}"
                    f"&end_date={reports.end_date:%Y-%m-%d}&export=xlsx"
                ),
            }
        )
        return context


def _reports_data_from_query(query) -> ReportsData:
    end_date = _date_from_query(query.get("end_date"))
    end_date = end_date or timezone.localdate()
    start_date = _date_from_query(query.get("start_date"))
    start_date = start_date or end_date - timedelta(days=30)
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    due_date_tasks = tuple(tasks_due_between(start_date, end_date))

    return ReportsData(
        start_date=start_date,
        end_date=end_date,
        due_date_tasks=due_date_tasks,
        status_counts=tasks_by_status(due_date_tasks),
        overdue_tasks=tuple(overdue_tasks(start_date=start_date, end_date=end_date)),
        workload=workload_by_assignee(due_date_tasks),
        productivity=productivity_by_area(start_date, end_date),
        deadline=deadline_compliance(start_date, end_date),
    )


def _xlsx_response(reports: ReportsData) -> HttpResponse:
    workbook = build_reports_workbook(
        start_date=reports.start_date,
        end_date=reports.end_date,
        status_counts=reports.status_counts,
        overdue_tasks=reports.overdue_tasks,
        workload=reports.workload,
        productivity=reports.productivity,
        deadline=reports.deadline,
        due_date_tasks=reports.due_date_tasks,
    )
    filename = (
        f"reportes-jawinsa-{reports.start_date:%Y-%m-%d}-"
        f"a-{reports.end_date:%Y-%m-%d}.xlsx"
    )
    response = HttpResponse(
        workbook,
        content_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _date_from_query(value: str | None):
    return parse_date(value) if value else None
