"""Forms for the sales module."""

from django import forms

from src.clients.selectors import clients_list
from src.employees.selectors import active_employees
from src.sales.models import ServiceOrder
from src.vehicles.selectors import vehicles_list


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ["client", "vehicle", "advisor", "description", "status"]
        labels = {
            "client": "Cliente",
            "vehicle": "Vehiculo",
            "advisor": "Asesor",
            "description": "Trabajo acordado",
            "status": "Estado",
        }
        help_texts = {
            "advisor": "Opcional. Use el asesor que negocio el servicio.",
            "description": "Describa lo acordado con el cliente.",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = clients_list()
        self.fields["client"].empty_label = "Seleccione un cliente"
        self.fields["vehicle"].queryset = vehicles_list()
        self.fields["vehicle"].empty_label = "Seleccione un vehiculo"
        self.fields["advisor"].queryset = active_employees()
        self.fields["advisor"].empty_label = "Sin asesor asignado"

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get("client")
        vehicle = cleaned_data.get("vehicle")
        if client and vehicle and vehicle.client_id != client.id:
            self.add_error(
                "vehicle",
                "Seleccione un vehiculo que pertenezca al cliente.",
            )
        return cleaned_data
