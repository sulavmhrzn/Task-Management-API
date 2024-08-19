from rest_framework import permissions


class IsAdminUserOrCreateOnly(permissions.BasePermission):
    """
    Used to create/signup a user.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_superuser


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    If current users role is manager. Grant create permission.
    else, Grant Read permission only.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_manager()


class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    """
    If current user is owner of the project. Grant Read, Update and delete permissions.
    If current user is in assigned_developers. Grant Read permission.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return obj.created_by == request.user or request.user in obj.team.all()
        return obj.created_by == request.user


class IsTaskOwnerOrAssignedDeveloper(permissions.BasePermission):
    """
    If current user is owner of the task. Grant Read, Update and delete permissions.
    If current user is in assigned_developers. Grant Read and Update pemissions.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        if request.method == "DELETE":
            return obj.created_by == request.user

        return (
            obj.created_by == request.user
            or request.user in obj.assigned_developers.all()
        )


class IsManagerRole(permissions.BasePermission):
    """
    Requires manager role
    """

    def has_permission(self, request, view):
        return request.user.is_manager()
