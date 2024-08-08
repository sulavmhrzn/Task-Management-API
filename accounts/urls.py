from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.UserListCreateView.as_view(), name="users"),
    # path("create/", views.UserCreateView.as_view(), name="user-create"),
]
