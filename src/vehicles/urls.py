"""URL routes for the vehicles module."""

from django.urls import path

from src.vehicles import views

app_name = "vehicles"

urlpatterns = [
    path("", views.VehicleListView.as_view(), name="list"),
    path("new/", views.VehicleCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="edit"),
]
