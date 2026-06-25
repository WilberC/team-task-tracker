"""Forms for the areas module."""

from django import forms

from src.areas.models import Area


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["name", "description", "active"]
        labels = {
            "name": "Nombre del area",
            "description": "Descripcion",
            "active": "Disponible para nuevas asignaciones",
        }
        help_texts = {
            "description": "Use una descripcion breve para que el equipo la reconozca.",
            "active": "Las areas inactivas no aparecen en selectores de asignacion.",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
