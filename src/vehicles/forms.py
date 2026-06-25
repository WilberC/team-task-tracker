"""Forms for the vehicles module."""

from django import forms

from src.clients.selectors import clients_list
from src.vehicles.models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["client", "plate", "make", "model", "year"]
        labels = {
            "client": "Cliente",
            "plate": "Placa",
            "make": "Marca",
            "model": "Modelo",
            "year": "Anio",
        }
        help_texts = {
            "plate": "Use la placa visible del vehiculo. Ejemplo: ABC-123.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["client"].queryset = clients_list()
        self.fields["client"].empty_label = "Seleccione un cliente"

    def clean_plate(self) -> str:
        return self.cleaned_data["plate"].strip().upper()
