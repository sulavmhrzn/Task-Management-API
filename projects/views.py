from rest_framework import generics, permissions

from common.permissions import IsManagerOrReadOnly
from projects.models import Project

from .serializers import ProjectSerializer


class ProjectListCreateSerializer(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
