"""URL routes for the teams module."""

from django.urls import path

from src.teams import views

app_name = "teams"

urlpatterns = [
    path("", views.TeamListView.as_view(), name="list"),
    path("new/", views.TeamCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.TeamUpdateView.as_view(), name="edit"),
]
