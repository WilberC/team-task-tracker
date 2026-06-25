"""Root URL configuration for Team Task Tracker."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from src.workshop.views import ClientStatusView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("status/<uuid:token>/", ClientStatusView.as_view(), name="client_status"),
    path("admin/", admin.site.urls),
    path("clients/", include("src.clients.urls")),
    path("vehicles/", include("src.vehicles.urls")),
    path("sales/", include("src.sales.urls")),
    path("workshop/", include("src.workshop.urls")),
    path("tasks/", include("src.tasks.urls")),
    path("dashboard/", include("src.dashboard.urls")),
    path("reports/", include("src.reports.urls")),
    path("areas/", include("src.areas.urls")),
    path("employees/", include("src.employees.urls")),
    path("teams/", include("src.teams.urls")),
]
