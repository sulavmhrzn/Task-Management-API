from django.urls import path

from accounts import views

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user-list"),
]
