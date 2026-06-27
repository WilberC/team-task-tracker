# Team Task Tracker

A web system for a **mechanic workshop** ("taller mecánico"). It tracks the work
on each interned vehicle — from the **service order** negotiated with the client,
to the **job order**, down to the individual **tasks** (and subtasks) each
mechanic or team performs — so the shop knows who is doing what and the client
can follow their vehicle's progress.

The work has two parts (see [Domain](docs/domain.md)):

- **Part 1 — Front desk:** advisor negotiates the work and records a service
  order. Kept simple for now.
- **Part 2 — Workshop (the priority):** the service order generates a job order;
  the vehicle is interned and the work is broken into assigned, status-tracked
  tasks.

It is built for **non-technical users**, so the interface must be clear and the
experience simple — see [UX & UI Principles](docs/ux-principles.md).

> **Status:** Phase 0 scaffold is implemented. The app runs as an empty Django
> project with PostgreSQL, admin, Docker, and the frontend build in place.

## Why this exists

In a workshop, work is often coordinated informally through messages or word of
mouth, causing unclear ownership, hard-to-track delays, poor visibility of each
mechanic's workload, and no easy way for clients to know their vehicle's status.
Team Task Tracker centralizes that work in one place.

## Tech stack at a glance

| Layer        | Technology                          |
| ------------ | ----------------------------------- |
| Backend      | Django (Python)                     |
| Database     | PostgreSQL                          |
| Rendering    | Django Templates + htmx             |
| Client-side  | TypeScript (minimal)                |
| Styling      | SCSS + Open Props                   |
| Python deps  | uv                                  |
| Frontend deps| pnpm                                |
| Optional     | Django Channels + WebSockets        |

See [docs/tech-stack.md](docs/tech-stack.md) for the full rationale.

## Local development

Install dependencies:

```bash
uv sync
pnpm install
```

Start PostgreSQL:

```bash
docker compose up -d db
```

Run migrations and create the local admin user:

```bash
uv run python manage.py migrate
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@example.com \
DJANGO_SUPERUSER_PASSWORD=admin \
uv run python manage.py createsuperuser --noinput
```

Build frontend assets and run the app:

```bash
pnpm build
uv run python manage.py runserver
```

The development commands are also available in the `justfile`, for example
`just db`, `just migrate`, `just frontend`, and `just run`.

## Creating modules

Use the project scaffold command instead of Django's default `startapp`:

```bash
uv run python manage.py startmodule tasks
```

The command creates the module layout documented in
[Architecture → Module scaffolding](docs/architecture.md#module-scaffolding).
After creating a module, register its app config in `INSTALLED_APPS`, for
example `src.tasks.apps.TasksConfig`.

## Documentation

The full specification lives in [`docs/`](docs/), split by concern:

| Document | What it covers |
| -------- | -------------- |
| [Overview](docs/overview.md)         | Problem, objective, scope, and expected results |
| [Domain](docs/domain.md)             | The auto repair workshop context: service orders, job orders, two parts |
| [UX & UI Principles](docs/ux-principles.md) | Designing for non-technical users: clarity-first guidelines |
| [Features](docs/features.md)         | Job orders, tasks, subtasks, assignment, client view, screens |
| [Workflows](docs/workflows.md)       | Workshop flow, task lifecycle, and end-to-end flow (diagrams) |
| [Data Model](docs/data-model.md)     | Entities and relationships (ER diagram) |
| [Reports](docs/reports.md)           | The five reports the system produces |
| [Tech Stack](docs/tech-stack.md)     | Each technology and where it is used |
| [Architecture](docs/architecture.md) | Repository layout, Django modules, templates, assets (diagram) |
| [Paradigms](docs/paradigms.md)       | How OOP, functional, and structured programming are applied |
| [Deployment](docs/deployment.md)     | Production environment, release, smoke-test, and rollback steps |
| [Implementation Plan](docs/implementation/README.md) | Phased build plan with checkable task lists |

## Diagrams

Diagrams are written in [PlantUML](https://plantuml.com/) inside fenced
` ```plantuml ` blocks. Render them with the PlantUML CLI, a PlantUML server,
or an editor extension (e.g. VS Code "PlantUML"). Example:

```bash
plantuml docs/**/*.md
```
