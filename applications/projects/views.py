from rest_framework import generics, pagination, permissions

from common.permissions import IsManagerOrReadOnly, IsProjectOwnerOrReadOnly

from .models import Project
from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related("team").all()
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProjectRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = (
        Project.objects.prefetch_related("team").select_related("created_by").all()
    )
    permission_classes = [permissions.IsAuthenticated, IsProjectOwnerOrReadOnly]
