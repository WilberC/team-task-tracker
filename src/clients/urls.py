"""URL routes for the clients module."""

from django.urls import path

from src.clients import views

app_name = "clients"

urlpatterns = [
    path("", views.ClientListView.as_view(), name="list"),
    path("new/", views.ClientCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ClientUpdateView.as_view(), name="edit"),
]
