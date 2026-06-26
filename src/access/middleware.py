"""Middleware for role-aware admin access."""

from django.core.exceptions import PermissionDenied

from src.access.roles import is_administrator


class AdminRoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith("/admin/")
            and request.user.is_authenticated
            and not is_administrator(request.user)
        ):
            raise PermissionDenied("No tiene permiso para acceder al admin.")
        return self.get_response(request)
