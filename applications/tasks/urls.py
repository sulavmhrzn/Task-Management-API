from django.urls import path

from . import views

urlpatterns = [
    path("", views.TaskListCreateView.as_view(), name="tasks-list-create"),
    path("<int:pk>/audit/", views.AuditLogsListView.as_view(), name="audit-list"),
    path(
        "<int:pk>/audit/download",
        views.AuditLogDownloadView.as_view(),
        name="audit-download",
    ),
    path(
        "<int:pk>/",
        views.TaskRetrieveUpdateDeleteView.as_view(),
        name="tasks-retrieve-update-delete",
    ),
]
