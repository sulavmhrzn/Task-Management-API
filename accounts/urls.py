from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.UserListCreateView.as_view(), name="users"),
    path("me/", views.UserDashboardView.as_view(), name="dashboard"),
]
