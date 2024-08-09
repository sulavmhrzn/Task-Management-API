from rest_framework import generics, permissions

from common.permissions import IsManagerOrReadOnly, IsTaskOwnerOrAssignedDeveloper
from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskUpdateSerializerForDeveloper


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# If user is a manager then request body should include all the necessary fields
# else validation errors are raised. I currently have no idea how to fix this.
class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        IsTaskOwnerOrAssignedDeveloper,
    ]

    def get_serializer_class(self):
        if self.request.user.is_developer() and self.request.method in ["PATCH", "PUT"]:
            return TaskUpdateSerializerForDeveloper
        return super().get_serializer_class()
