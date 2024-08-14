from django.urls import path

from . import views

urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name="tasks-list-create"),
    path(
        "<int:pk>/",
        views.TaskRetrieveUpdateDeleteView.as_view(),
        name="tasks-retrieve-update-delete",
    ),
]
