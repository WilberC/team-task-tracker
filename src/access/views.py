"""Views for authentication flow helpers."""

import secrets

from django.conf import settings
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from src.access.forms import EmailOrUsernameAuthenticationForm
from src.access.roles import access_flags

TEST_ACCOUNTS_SESSION_KEY = "test_accounts_unlocked"
TEST_ACCOUNTS_ERROR_KEY = "test_accounts_unlock_error"
TEST_ACCOUNTS_SESSION_AGE = 60 * 60 * 24 * 30


class InternalLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True
    authentication_form = EmailOrUsernameAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(test_accounts_context(self.request))
        return context


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


class TestAccountsUnlockView(View):
    def post(self, request):
        if not test_accounts_available():
            raise Http404()

        submitted_password = request.POST.get("unlock_password", "")
        if secrets.compare_digest(
            submitted_password,
            settings.TEST_ACCOUNTS_UNLOCK_PASSWORD,
        ):
            request.session[TEST_ACCOUNTS_SESSION_KEY] = True
            request.session.pop(TEST_ACCOUNTS_ERROR_KEY, None)
            request.session.set_expiry(TEST_ACCOUNTS_SESSION_AGE)
        else:
            request.session[TEST_ACCOUNTS_SESSION_KEY] = False
            request.session[TEST_ACCOUNTS_ERROR_KEY] = "Clave de acceso incorrecta."

        return redirect(reverse("login"))


def test_accounts_available() -> bool:
    return bool(
        _test_account_emails()
        and settings.SEED_USER_PASSWORD
        and settings.TEST_ACCOUNTS_UNLOCK_PASSWORD
    )


def test_accounts_context(request) -> dict:
    available = test_accounts_available()
    unlocked = bool(available and request.session.get(TEST_ACCOUNTS_SESSION_KEY))
    context = {
        "test_accounts_available": available,
        "test_accounts_unlocked": unlocked,
        "test_accounts_error": request.session.pop(TEST_ACCOUNTS_ERROR_KEY, ""),
    }
    if unlocked:
        context.update(
            {
                "test_account_emails": _test_account_emails(),
                "test_account_password": settings.SEED_USER_PASSWORD,
            }
        )
    return context


def _test_account_emails() -> list[str]:
    return [email.strip() for email in settings.TEST_ACCOUNT_EMAILS if email.strip()]
