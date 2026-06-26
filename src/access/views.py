"""Views for authentication flow helpers."""

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views import View

from src.access.roles import access_flags


class PostLoginRedirectView(View):
    def get(self, request):
        flags = access_flags(request.user)
        if flags.can_view_dashboard:
            return redirect("dashboard:index")
        if flags.can_view_tasks:
            return redirect("tasks:list")
        if flags.can_view_sales:
            return redirect("sales:list")
        if flags.can_view_workshop:
            return redirect("workshop:list")
        raise PermissionDenied("Su usuario no tiene un rol interno asignado.")
