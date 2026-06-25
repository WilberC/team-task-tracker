"""URL routes for the sales module."""

from django.urls import path

from src.sales import views

app_name = "sales"

urlpatterns = [
    path("", views.ServiceOrderListView.as_view(), name="list"),
    path("new/", views.ServiceOrderCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.ServiceOrderUpdateView.as_view(), name="edit"),
]
