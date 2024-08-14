from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiRootView(APIView):
    """
    Root api view. Lists all available routes
    """

    def get(self, request, *args, **kwargs):
        routes = {
            "admin": {
                "list users": request.build_absolute_uri(reverse("users")),
            },
            "accounts": {
                "create user": request.build_absolute_uri(reverse("users")),
                "dashboard": request.build_absolute_uri(reverse("dashboard")),
            },
            "authentication": {
                "obtain token": request.build_absolute_uri(
                    reverse("obtain_auth_token")
                ),
                "logout": request.build_absolute_uri(reverse("logout_view")),
            },
            "projects": {
                "create project": request.build_absolute_uri(
                    reverse("projects-list-create")
                ),
                "list projects": request.build_absolute_uri(
                    reverse("projects-list-create")
                ),
                "retrieve project": request.build_absolute_uri(
                    reverse("projects-retrieve-update-delete", args=[0])
                ),
                "update project": request.build_absolute_uri(
                    reverse("projects-retrieve-update-delete", kwargs={"pk": 0})
                ),
                "delete project": request.build_absolute_uri(
                    reverse("projects-retrieve-update-delete", kwargs={"pk": 0})
                ),
            },
            "tasks": {
                "create task": request.build_absolute_uri(reverse("tasks-list-create")),
                "list tasks": request.build_absolute_uri(reverse("tasks-list-create")),
                "retrieve task": request.build_absolute_uri(
                    reverse("tasks-retrieve-update-delete", kwargs={"pk": 0})
                ),
                "update task": request.build_absolute_uri(
                    reverse("tasks-retrieve-update-delete", kwargs={"pk": 0})
                ),
                "delete task": request.build_absolute_uri(
                    reverse("tasks-retrieve-update-delete", kwargs={"pk": 0})
                ),
            },
        }
        return Response(routes)
