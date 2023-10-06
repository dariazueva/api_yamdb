from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (
                request.user.is_superuser
                or request.user.role == 'admin'
            )
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_superuser
                or request.user.role == 'admin')
        )


class IsAuthorModeratorAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (obj.author == request.user
                    or request.user.is_superuser
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator')
        return request.method in permissions.SAFE_METHODS
