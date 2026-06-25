"""URL routes for the tasks module."""

from django.urls import path

from src.tasks import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="list"),
    path("kanban/", views.TaskKanbanView.as_view(), name="kanban"),
    path(
        "job-orders/<int:job_order_pk>/new/",
        views.TopLevelTaskCreateView.as_view(),
        name="create",
    ),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="edit"),
    path("<int:pk>/status/", views.TaskStatusUpdateView.as_view(), name="status"),
    path("<int:pk>/cancel/", views.TaskCancelView.as_view(), name="cancel"),
    path(
        "<int:parent_pk>/subtasks/new/",
        views.SubtaskCreateView.as_view(),
        name="create_subtask",
    ),
]
