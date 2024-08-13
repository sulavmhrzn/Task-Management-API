from rest_framework import generics, permissions

from common.mail import send_create_task_mail
from common.permissions import IsManagerOrReadOnly, IsTaskOwnerOrAssignedDeveloper

from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializerForDeveloper


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
