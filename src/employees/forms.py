"""Forms for the employees module."""

from django import forms

from src.areas.selectors import active_areas
from src.employees.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["full_name", "email", "area", "position", "active"]
        labels = {
            "full_name": "Nombre completo",
            "email": "Correo",
            "area": "Area de trabajo",
            "position": "Cargo",
            "active": "Disponible para nuevas asignaciones",
        }
        help_texts = {
            "active": (
                "Los empleados inactivos no aparecen en selectores de asignacion."
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        area_queryset = active_areas()
        if self.instance.pk and self.instance.area_id:
            area_queryset = area_queryset | self.instance.area.__class__.objects.filter(
                pk=self.instance.area_id
            )
        self.fields["area"].queryset = area_queryset.distinct()
        self.fields["area"].empty_label = "Seleccione un area"
