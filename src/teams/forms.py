"""Forms for the teams module."""

from django import forms

from src.areas.selectors import active_areas
from src.employees.selectors import active_employees
from src.teams.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "area", "members", "active"]
        labels = {
            "name": "Nombre del equipo",
            "area": "Area de trabajo",
            "members": "Integrantes",
            "active": "Disponible para nuevas asignaciones",
        }
        help_texts = {
            "members": "Seleccione solo empleados del area del equipo.",
            "active": "Los equipos inactivos no aparecen en selectores de asignacion.",
        }
        widgets = {
            "members": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        area_queryset = active_areas()
        member_queryset = active_employees()
        if self.instance.pk and self.instance.area_id:
            area_model = self.instance.area.__class__
            area_queryset = area_queryset | area_model.objects.filter(
                pk=self.instance.area_id
            )
            member_queryset = member_queryset | self.instance.members.all()
        self.fields["area"].queryset = area_queryset.distinct()
        self.fields["area"].empty_label = "Seleccione un area"
        self.fields["members"].queryset = member_queryset.distinct()

    def clean_members(self):
        members = self.cleaned_data["members"]
        area = self.cleaned_data.get("area")
        if area and members.exclude(area=area).exists():
            raise forms.ValidationError(
                "Seleccione solo empleados que pertenezcan al area del equipo."
            )
        return members
