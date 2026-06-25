"""URL routes for reports."""

from django.urls import path

from src.reports import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportsView.as_view(), name="index"),
]
