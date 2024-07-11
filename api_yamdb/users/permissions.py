from rest_framework.permissions import BasePermission


class IsAdminOrSuper(BasePermission):
    message = 'Доступ разрешен администратору'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_admin
        )