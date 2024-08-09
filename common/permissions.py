from rest_framework import permissions


class IsAdminUserOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_superuser


class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_manager()


class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return obj.created_by == request.user or request.user in obj.team.all()
        return obj.created_by == request.user
