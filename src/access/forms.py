"""Authentication forms for internal access."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import TextInput


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Usuario o correo",
        widget=TextInput(attrs={"autofocus": True}),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        if username and "@" in username:
            user = (
                get_user_model()
                ._default_manager.filter(email__iexact=username)
                .order_by("pk")
                .first()
            )
            if user:
                self.cleaned_data["username"] = user.get_username()
        return super().clean()
