"""Forms for the clients module."""

from django import forms

from src.clients.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["full_name", "phone", "email"]
        labels = {
            "full_name": "Nombre completo",
            "phone": "Telefono",
            "email": "Correo",
        }
        help_texts = {
            "email": "Opcional. Se usara mas adelante para la vista del cliente.",
        }
