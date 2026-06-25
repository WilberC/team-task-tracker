"""Forms for the tasks module."""

from django import forms

from src.areas.selectors import active_areas
from src.employees.selectors import active_employees
from src.tasks.models import Task, TaskPriority, TaskStatus
from src.teams.selectors import active_teams
from src.workshop.selectors import open_job_orders


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "area",
            "assigned_employee",
            "assigned_team",
            "priority",
            "start_date",
            "due_date",
        ]
        labels = {
            "title": "Titulo",
            "description": "Descripcion",
            "area": "Area",
            "assigned_employee": "Empleado responsable",
            "assigned_team": "Equipo responsable",
            "priority": "Prioridad",
            "start_date": "Fecha de inicio",
            "due_date": "Fecha limite",
        }
        help_texts = {
            "assigned_employee": "Seleccione empleado o equipo, no ambos.",
            "due_date": "Use la fecha comprometida para controlar vencimientos.",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, job_order=None, parent_task=None, **kwargs):
        self.job_order = job_order
        self.parent_task = parent_task
        super().__init__(*args, **kwargs)
        if job_order:
            self.instance.job_order = job_order
        if parent_task:
            self.instance.parent_task = parent_task
        self.fields["area"].queryset = active_areas()
        self.fields["area"].empty_label = "Seleccione un area"
        self.fields["assigned_employee"].queryset = active_employees()
        self.fields["assigned_employee"].empty_label = "Sin empleado"
        self.fields["assigned_team"].queryset = active_teams()
        self.fields["assigned_team"].empty_label = "Sin equipo"
        if parent_task:
            self.fields["area"].required = False
            self.fields[
                "area"
            ].help_text = "Si lo deja vacio, usara el area de la tarea principal."

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get("assigned_employee")
        team = cleaned_data.get("assigned_team")
        if bool(employee) == bool(team):
            raise forms.ValidationError(
                "Seleccione exactamente un responsable: empleado o equipo."
            )
        if self.parent_task and not cleaned_data.get("area"):
            cleaned_data["area"] = self.parent_task.area
        return cleaned_data


class TaskFilterForm(forms.Form):
    job_order = forms.ModelChoiceField(
        label="Orden de trabajo",
        queryset=open_job_orders(),
        required=False,
        empty_label="Todas",
    )
    area = forms.ModelChoiceField(
        label="Area",
        queryset=active_areas(),
        required=False,
        empty_label="Todas",
    )
    assigned_employee = forms.ModelChoiceField(
        label="Empleado",
        queryset=active_employees(),
        required=False,
        empty_label="Todos",
    )
    assigned_team = forms.ModelChoiceField(
        label="Equipo",
        queryset=active_teams(),
        required=False,
        empty_label="Todos",
    )
    status = forms.ChoiceField(
        label="Estado",
        choices=[("", "Todos"), *TaskStatus.choices],
        required=False,
    )
    priority = forms.ChoiceField(
        label="Prioridad",
        choices=[("", "Todas"), *TaskPriority.choices],
        required=False,
    )
    due_date = forms.DateField(
        label="Fecha limite",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_order"].queryset = open_job_orders()
        self.fields["area"].queryset = active_areas()
        self.fields["assigned_employee"].queryset = active_employees()
        self.fields["assigned_team"].queryset = active_teams()
