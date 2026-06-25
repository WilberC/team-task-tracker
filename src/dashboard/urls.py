"""URL routes for dashboard."""

from django.urls import path

from src.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),
]
