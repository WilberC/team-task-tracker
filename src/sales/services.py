"""Write orchestration for the sales module."""

from django.core.exceptions import ValidationError

from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.vehicles.models import Vehicle


def create_service_order(
    *,
    client: Client,
    vehicle: Vehicle,
    description: str,
    advisor: Employee | None = None,
    status: str = ServiceOrderStatus.OPEN,
) -> ServiceOrder:
    if vehicle.client_id != client.id:
        raise ValidationError("El vehiculo seleccionado no pertenece al cliente.")

    return ServiceOrder.objects.create(
        client=client,
        vehicle=vehicle,
        advisor=advisor,
        description=description,
        status=status,
    )
