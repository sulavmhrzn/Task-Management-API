from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProjectListCreateView.as_view(), name="projects-list-create"),
    path(
        "<int:pk>/",
        views.ProjectRetrieveUpdateView.as_view(),
        name="projects-retrieve-update-delete",
    ),
]
