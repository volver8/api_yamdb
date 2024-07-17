from rest_framework import permissions


class IsAdminOrSuper(permissions.BasePermission):
    """Проверка наличия прав администратора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка наличия прав администратора."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin)


class AuthorOrReadOnly(permissions.BasePermission):
    """Проверка наличия прав автора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
