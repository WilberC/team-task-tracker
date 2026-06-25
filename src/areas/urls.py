"""URL routes for the areas module."""

from django.urls import path

from src.areas import views

app_name = "areas"

urlpatterns = [
    path("", views.AreaListView.as_view(), name="list"),
    path("new/", views.AreaCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.AreaUpdateView.as_view(), name="edit"),
]
