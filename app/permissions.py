from rest_framework.permissions import BasePermission


def Has_role(*roles):
    class RolePermission(BasePermission):
        def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role in roles
    return RolePermission
