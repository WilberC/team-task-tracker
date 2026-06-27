"""Seed the project with Spanish demo data."""

from datetime import timedelta
from io import StringIO

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from src.access.roles import (
    ADMINISTRATOR,
    FRONT_DESK,
    MECHANIC,
    REPORTS_VIEWER,
    SERVICE_ADVISOR,
    WORKSHOP_SUPERVISOR,
)
from src.areas.models import Area
from src.clients.models import Client
from src.employees.models import Employee
from src.sales.models import ServiceOrder, ServiceOrderStatus
from src.tasks.models import Task, TaskPriority, TaskStatus
from src.teams.models import Team
from src.vehicles.models import Vehicle
from src.workshop.models import JobOrder, JobOrderStatus
from src.workshop.services import refresh_job_order_status

SEED_USERNAMES = (
    "administrador",
    "recepcion",
    "asesor",
    "supervisor",
    "mecanico",
    "mecanico_pintura",
    "reportes",
)

AREA_DATA = (
    (
        "Recepcion",
        "Atencion inicial, registro de clientes y coordinacion de ingreso.",
    ),
    (
        "Administracion",
        "Gestion interna, seguimiento operativo y reportes de taller.",
    ),
    (
        "Mecanica",
        "Diagnostico, mantenimiento preventivo y reparaciones mecanicas.",
    ),
    (
        "Electricidad",
        "Diagnostico electrico, sensores, cableado y sistemas electronicos.",
    ),
    (
        "Carroceria y Pintura",
        "Reparacion de latoneria, preparacion, pintura y acabados.",
    ),
)

USER_DATA = (
    {
        "username": "administrador",
        "first_name": "Administrador",
        "last_name": "Jawinsa",
        "email": "administrador@jawinsa.test",
        "role": ADMINISTRATOR,
        "area": "Administracion",
        "position": "Administrador del sistema",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "recepcion",
        "first_name": "Rosa",
        "last_name": "Quispe",
        "email": "recepcion@jawinsa.test",
        "role": FRONT_DESK,
        "area": "Recepcion",
        "position": "Recepcionista",
    },
    {
        "username": "asesor",
        "first_name": "Miguel",
        "last_name": "Salazar",
        "email": "asesor@jawinsa.test",
        "role": SERVICE_ADVISOR,
        "area": "Recepcion",
        "position": "Asesor de servicio",
    },
    {
        "username": "supervisor",
        "first_name": "Patricia",
        "last_name": "Ramos",
        "email": "supervisor@jawinsa.test",
        "role": WORKSHOP_SUPERVISOR,
        "area": "Mecanica",
        "position": "Supervisora de taller",
    },
    {
        "username": "mecanico",
        "first_name": "Carlos",
        "last_name": "Vargas",
        "email": "mecanico@jawinsa.test",
        "role": MECHANIC,
        "area": "Mecanica",
        "position": "Mecanico automotriz",
    },
    {
        "username": "mecanico_pintura",
        "first_name": "Luis",
        "last_name": "Mendoza",
        "email": "pintura@jawinsa.test",
        "role": MECHANIC,
        "area": "Carroceria y Pintura",
        "position": "Tecnico de carroceria y pintura",
    },
    {
        "username": "reportes",
        "first_name": "Elena",
        "last_name": "Torres",
        "email": "reportes@jawinsa.test",
        "role": REPORTS_VIEWER,
        "area": "Administracion",
        "position": "Analista de reportes",
    },
)

TEAM_DATA = (
    {
        "name": "Equipo Mecanica Rapida",
        "area": "Mecanica",
        "members": ("mecanico", "supervisor"),
    },
    {
        "name": "Equipo Electricidad y Diagnostico",
        "area": "Electricidad",
        "members": (),
    },
    {
        "name": "Equipo Carroceria Ligera",
        "area": "Carroceria y Pintura",
        "members": ("mecanico_pintura",),
    },
)

CLIENT_DATA = (
    {
        "full_name": "Ana Maria Flores",
        "phone": "999 241 118",
        "email": "ana.flores@example.test",
        "vehicle": {
            "plate": "ABC-123",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
        },
        "advisor": "asesor",
        "description": (
            "Revision general por ruido en suspension delantera y mantenimiento "
            "preventivo de 40 000 km."
        ),
        "service_status": ServiceOrderStatus.APPROVED,
        "job_status": JobOrderStatus.IN_PROGRESS,
        "days_offset": -2,
    },
    {
        "full_name": "Jorge Luis Castillo",
        "phone": "987 654 321",
        "email": "jorge.castillo@example.test",
        "vehicle": {
            "plate": "BDF-456",
            "make": "Nissan",
            "model": "Frontier",
            "year": 2019,
        },
        "advisor": "asesor",
        "description": (
            "Ingreso por perdida de potencia, luz de motor encendida y revision "
            "del sistema electrico."
        ),
        "service_status": ServiceOrderStatus.APPROVED,
        "job_status": JobOrderStatus.OPEN,
        "days_offset": -1,
    },
    {
        "full_name": "Mariela Gutierrez",
        "phone": "956 112 808",
        "email": "mariela.gutierrez@example.test",
        "vehicle": {
            "plate": "CGA-789",
            "make": "Hyundai",
            "model": "Tucson",
            "year": 2021,
        },
        "advisor": "asesor",
        "description": (
            "Cambio de aceite, filtros, inspeccion de frenos y entrega el mismo dia."
        ),
        "service_status": ServiceOrderStatus.CLOSED,
        "job_status": JobOrderStatus.DELIVERED,
        "days_offset": -7,
    },
    {
        "full_name": "Empresa Transportes Andinos",
        "phone": "944 300 221",
        "email": "operaciones@andinos.example.test",
        "vehicle": {
            "plate": "TAD-204",
            "make": "Mitsubishi",
            "model": "L200",
            "year": 2018,
        },
        "advisor": "asesor",
        "description": (
            "Reparacion de golpe lateral derecho, alineamiento de paneles y pintura."
        ),
        "service_status": ServiceOrderStatus.APPROVED,
        "job_status": JobOrderStatus.IN_PROGRESS,
        "days_offset": -4,
    },
)

TASK_DATA = {
    "ABC-123": (
        {
            "title": "Diagnostico de suspension delantera",
            "description": "Verificar bujes, amortiguadores y terminales de direccion.",
            "area": "Mecanica",
            "employee": "mecanico",
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.IN_PROGRESS,
            "start_offset": -2,
            "due_offset": 1,
            "subtasks": (
                {
                    "title": "Inspeccion visual en elevador",
                    "description": "Revisar holguras, fugas y desgaste irregular.",
                    "employee": "mecanico",
                    "status": TaskStatus.COMPLETED,
                    "due_offset": -1,
                },
                {
                    "title": "Prueba de ruta controlada",
                    "description": "Confirmar ruido en baches y frenadas suaves.",
                    "employee": "mecanico",
                    "status": TaskStatus.IN_PROGRESS,
                    "due_offset": 1,
                },
            ),
        },
        {
            "title": "Mantenimiento preventivo de 40 000 km",
            "description": "Cambiar aceite, filtros y revisar niveles de fluidos.",
            "area": "Mecanica",
            "team": "Equipo Mecanica Rapida",
            "priority": TaskPriority.MEDIUM,
            "status": TaskStatus.PENDING,
            "start_offset": 0,
            "due_offset": 2,
            "subtasks": (),
        },
    ),
    "BDF-456": (
        {
            "title": "Escaneo electronico del motor",
            "description": "Leer codigos de falla y registrar parametros en vivo.",
            "area": "Electricidad",
            "employee": "supervisor",
            "priority": TaskPriority.CRITICAL,
            "status": TaskStatus.OVERDUE,
            "start_offset": -3,
            "due_offset": -1,
            "subtasks": (),
        },
    ),
    "CGA-789": (
        {
            "title": "Servicio preventivo completo",
            "description": "Ejecutar mantenimiento pactado y preparar entrega.",
            "area": "Mecanica",
            "team": "Equipo Mecanica Rapida",
            "priority": TaskPriority.LOW,
            "status": TaskStatus.COMPLETED,
            "start_offset": -7,
            "due_offset": -6,
            "subtasks": (
                {
                    "title": "Cambio de aceite y filtros",
                    "description": "Registrar kilometraje y repuestos usados.",
                    "employee": "mecanico",
                    "status": TaskStatus.COMPLETED,
                    "due_offset": -6,
                },
                {
                    "title": "Inspeccion final de frenos",
                    "description": "Validar espesor de pastillas y nivel de liquido.",
                    "employee": "supervisor",
                    "status": TaskStatus.COMPLETED,
                    "due_offset": -6,
                },
            ),
        },
    ),
    "TAD-204": (
        {
            "title": "Reparacion de carroceria lateral",
            "description": (
                "Enderezar panel lateral, preparar superficie y aplicar pintura."
            ),
            "area": "Carroceria y Pintura",
            "team": "Equipo Carroceria Ligera",
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.IN_PROGRESS,
            "start_offset": -4,
            "due_offset": 3,
            "subtasks": (
                {
                    "title": "Desmontaje de molduras",
                    "description": "Retirar piezas sin danar seguros ni grapas.",
                    "employee": "mecanico_pintura",
                    "status": TaskStatus.COMPLETED,
                    "due_offset": -2,
                },
                {
                    "title": "Preparacion para pintura",
                    "description": "Masillar, lijar y limpiar panel antes de base.",
                    "employee": "mecanico_pintura",
                    "status": TaskStatus.IN_PROGRESS,
                    "due_offset": 1,
                },
            ),
        },
    ),
}


class Command(BaseCommand):
    help = "Populate the project with Spanish demo data and test users."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--password",
            default=None,
            help="Password for seeded test users. Defaults to SEED_USER_PASSWORD.",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete the known seeded records before loading them again.",
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        password = options["password"] or settings.SEED_USER_PASSWORD
        if not password:
            raise CommandError("Set SEED_USER_PASSWORD or pass --password.")

        if options["reset"]:
            self._reset_seed_data()

        call_command("setup_roles", stdout=StringIO(), verbosity=0)

        areas = self._seed_areas()
        users = self._seed_users(areas, password)
        employees = {
            username: user.employee_profile for username, user in users.items()
        }
        teams = self._seed_teams(areas, employees)
        clients, vehicles, service_orders, job_orders = self._seed_front_desk(
            employees,
        )
        self._seed_tasks(areas, employees, teams, vehicles, job_orders)
        self._refresh_job_orders(job_orders)

        self.stdout.write(
            self.style.SUCCESS(
                "Datos de prueba cargados: "
                f"{len(users)} usuarios, "
                f"{len(areas)} areas, "
                f"{len(clients)} clientes, "
                f"{len(vehicles)} vehiculos, "
                f"{len(service_orders)} ordenes de servicio, "
                f"{len(job_orders)} ordenes de trabajo."
            )
        )
        self.stdout.write(
            "Usuarios de prueba: "
            + ", ".join(SEED_USERNAMES)
            + f". Contrasena: {password}"
        )

    def _seed_areas(self) -> dict[str, Area]:
        areas = {}
        for name, description in AREA_DATA:
            area, _created = Area.objects.update_or_create(
                name=name,
                defaults={
                    "description": description,
                    "active": True,
                },
            )
            areas[name] = area
        return areas

    def _seed_users(
        self,
        areas: dict[str, Area],
        password: str,
    ) -> dict[str, User]:
        users = {}
        for data in USER_DATA:
            user, _created = User.objects.update_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                    "is_active": True,
                    "is_staff": data.get("is_staff", False),
                    "is_superuser": data.get("is_superuser", False),
                },
            )
            user.set_password(password)
            user.save()
            user.groups.set([Group.objects.get(name=data["role"])])

            Employee.objects.update_or_create(
                user=user,
                defaults={
                    "full_name": f"{data['first_name']} {data['last_name']}",
                    "email": data["email"],
                    "area": areas[data["area"]],
                    "position": data["position"],
                    "active": True,
                },
            )
            users[data["username"]] = user
        return users

    def _seed_teams(
        self,
        areas: dict[str, Area],
        employees: dict[str, Employee],
    ) -> dict[str, Team]:
        teams = {}
        for data in TEAM_DATA:
            team, _created = Team.objects.update_or_create(
                name=data["name"],
                area=areas[data["area"]],
                defaults={"active": True},
            )
            team.members.set([employees[username] for username in data["members"]])
            teams[data["name"]] = team
        return teams

    def _seed_front_desk(
        self,
        employees: dict[str, Employee],
    ) -> tuple[
        dict[str, Client],
        dict[str, Vehicle],
        dict[str, ServiceOrder],
        dict[str, JobOrder],
    ]:
        clients = {}
        vehicles = {}
        service_orders = {}
        job_orders = {}
        now = timezone.now()

        for data in CLIENT_DATA:
            client, _created = Client.objects.update_or_create(
                full_name=data["full_name"],
                defaults={
                    "phone": data["phone"],
                    "email": data["email"],
                },
            )
            vehicle_data = data["vehicle"]
            vehicle, _created = Vehicle.objects.update_or_create(
                plate=vehicle_data["plate"],
                defaults={
                    "client": client,
                    "make": vehicle_data["make"],
                    "model": vehicle_data["model"],
                    "year": vehicle_data["year"],
                },
            )
            service_order, _created = ServiceOrder.objects.update_or_create(
                vehicle=vehicle,
                description=data["description"],
                defaults={
                    "client": client,
                    "advisor": employees[data["advisor"]],
                    "status": data["service_status"],
                },
            )
            interned_at = now + timedelta(days=data["days_offset"])
            job_order, _created = JobOrder.objects.update_or_create(
                service_order=service_order,
                defaults={
                    "vehicle": vehicle,
                    "status": data["job_status"],
                    "interned_at": interned_at,
                    "closed_at": None,
                },
            )

            clients[client.full_name] = client
            vehicles[vehicle.plate] = vehicle
            service_orders[vehicle.plate] = service_order
            job_orders[vehicle.plate] = job_order
        return clients, vehicles, service_orders, job_orders

    def _seed_tasks(
        self,
        areas: dict[str, Area],
        employees: dict[str, Employee],
        teams: dict[str, Team],
        vehicles: dict[str, Vehicle],
        job_orders: dict[str, JobOrder],
    ) -> None:
        today = timezone.localdate()
        for plate, task_rows in TASK_DATA.items():
            job_order = job_orders[plate]
            for row in task_rows:
                task = self._upsert_task(
                    title=row["title"],
                    parent_task=None,
                    job_order=job_order,
                    area=areas[row["area"]],
                    employee=employees.get(row.get("employee", "")),
                    team=teams.get(row.get("team", "")),
                    priority=row["priority"],
                    status=row["status"],
                    description=row["description"],
                    start_date=today + timedelta(days=row["start_offset"]),
                    due_date=today + timedelta(days=row["due_offset"]),
                )
                for subtask_row in row["subtasks"]:
                    self._upsert_task(
                        title=subtask_row["title"],
                        parent_task=task,
                        job_order=None,
                        area=task.area,
                        employee=employees.get(subtask_row.get("employee", "")),
                        team=teams.get(subtask_row.get("team", "")),
                        priority=row["priority"],
                        status=subtask_row["status"],
                        description=subtask_row["description"],
                        start_date=today + timedelta(days=row["start_offset"]),
                        due_date=today + timedelta(days=subtask_row["due_offset"]),
                    )
            vehicles[plate].save(update_fields=["updated_at"])

    def _upsert_task(
        self,
        *,
        title: str,
        parent_task: Task | None,
        job_order: JobOrder | None,
        area: Area,
        employee: Employee | None,
        team: Team | None,
        priority: str,
        status: str,
        description: str,
        start_date,
        due_date,
    ) -> Task:
        lookup = {
            "title": title,
            "parent_task": parent_task,
            "job_order": job_order,
        }
        defaults = {
            "description": description,
            "area": area,
            "assigned_employee": employee,
            "assigned_team": team,
            "priority": priority,
            "status": status,
            "start_date": start_date,
            "due_date": due_date,
            "completion_date": (
                timezone.localdate() if status == TaskStatus.COMPLETED else None
            ),
        }
        task, _created = Task.objects.update_or_create(**lookup, defaults=defaults)
        return task

    def _refresh_job_orders(self, job_orders: dict[str, JobOrder]) -> None:
        for data in CLIENT_DATA:
            job_order = job_orders[data["vehicle"]["plate"]]
            refresh_job_order_status(job_order)
            job_order.status = data["job_status"]
            if data["job_status"] in (JobOrderStatus.DONE, JobOrderStatus.DELIVERED):
                job_order.closed_at = timezone.now()
            elif data["job_status"] != JobOrderStatus.DONE:
                job_order.closed_at = None
            job_order.save(update_fields=["status", "closed_at", "updated_at"])

    def _reset_seed_data(self) -> None:
        seeded_jobs = JobOrder.objects.filter(vehicle__plate__in=_vehicle_plates())
        Task.objects.filter(
            Q(job_order__in=seeded_jobs) | Q(parent_task__job_order__in=seeded_jobs),
        ).delete()
        JobOrder.objects.filter(vehicle__plate__in=_vehicle_plates()).delete()
        ServiceOrder.objects.filter(vehicle__plate__in=_vehicle_plates()).delete()
        Vehicle.objects.filter(plate__in=_vehicle_plates()).delete()
        Team.objects.filter(name__in=_team_names()).delete()
        Employee.objects.filter(user__username__in=SEED_USERNAMES).delete()
        User.objects.filter(username__in=SEED_USERNAMES).delete()
        Client.objects.filter(
            full_name__in=_client_names(),
            vehicles__isnull=True,
            service_orders__isnull=True,
        ).delete()


def _team_names() -> tuple[str, ...]:
    return tuple(data["name"] for data in TEAM_DATA)


def _client_names() -> tuple[str, ...]:
    return tuple(data["full_name"] for data in CLIENT_DATA)


def _vehicle_plates() -> tuple[str, ...]:
    return tuple(data["vehicle"]["plate"] for data in CLIENT_DATA)
