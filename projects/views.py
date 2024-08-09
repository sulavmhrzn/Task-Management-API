from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from common.permissions import IsManagerOrReadOnly, IsProjectOwnerOrReadOnly
from projects.models import Project

from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsProjectOwnerOrReadOnly]
