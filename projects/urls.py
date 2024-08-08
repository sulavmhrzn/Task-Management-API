from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProjectListCreateSerializer.as_view(), name="projects"),
]
