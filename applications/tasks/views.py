from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from common.mail import send_create_task_mail
from common.permissions import IsManagerOrReadOnly, IsTaskOwnerOrAssignedDeveloper

from .models import AuditLog, Task
from .serializers import (
    AuditLogSerializer,
    TaskSerializer,
    TaskUpdateSerializerForDeveloper,
)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.prefetch_related("assigned_developers").all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        send_create_task_mail(task)


# If user is a manager then request body should include all the necessary fields
# else validation errors are raised. I currently have no idea how to fix this.
class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = (
        Task.objects.prefetch_related("assigned_developers")
        .select_related("created_by")
        .all()
    )
    permission_classes = [
        permissions.IsAuthenticated,
        IsTaskOwnerOrAssignedDeveloper,
    ]

    def get_serializer_class(self):
        if self.request.user.is_developer() and self.request.method in ["PATCH", "PUT"]:
            return TaskUpdateSerializerForDeveloper
        return super().get_serializer_class()


class AuditLogsListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise PermissionDenied("Task does not exist.")
        if task.created_by != self.request.user:
            raise PermissionDenied(
                "You do not have permission to view these audit logs."
            )
        return AuditLog.objects.filter(task=task).all()
