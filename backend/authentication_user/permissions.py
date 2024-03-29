from rest_framework import permissions


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or view.action == 'create'
