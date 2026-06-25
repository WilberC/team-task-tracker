"""URL routes for the employees module."""

from django.urls import path

from src.employees import views

app_name = "employees"

urlpatterns = [
    path("", views.EmployeeListView.as_view(), name="list"),
    path("new/", views.EmployeeCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.EmployeeUpdateView.as_view(), name="edit"),
]
