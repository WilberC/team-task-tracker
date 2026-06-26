"""Template context for role-aware navigation and actions."""

from src.access.roles import access_flags


def access(request):
    return {"access": access_flags(request.user)}
