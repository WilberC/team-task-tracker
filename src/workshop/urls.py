"""URL routes for the workshop module."""

from django.urls import path

from src.workshop import views

app_name = "workshop"

urlpatterns = [
    path("", views.JobOrderListView.as_view(), name="list"),
    path("<int:pk>/", views.JobOrderDetailView.as_view(), name="detail"),
    path("<int:pk>/close/", views.JobOrderCloseView.as_view(), name="close"),
    path("<int:pk>/deliver/", views.JobOrderDeliverView.as_view(), name="deliver"),
]
