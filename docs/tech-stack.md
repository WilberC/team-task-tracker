# Tech Stack

[← Back to README](../README.md)

The system is a server-rendered Django application enhanced with htmx, with a
small amount of TypeScript for interactions that htmx cannot handle alone.

## Summary

| Layer                 | Technology                   | Where it is used |
| --------------------- | ---------------------------- | ---------------- |
| Backend framework     | Django                       | Application logic, models, views, forms, auth, reports |
| Language              | Python                       | Backend and business logic (OOP + functional + structured) |
| Python package manager| uv                           | Virtual environment and dependency management |
| Database              | PostgreSQL                   | Areas, employees, tasks, priorities, statuses, report data |
| Frontend rendering    | Django Templates             | Dashboard, lists, forms, Kanban board, reports |
| Frontend interaction  | htmx                         | Dynamic updates without full page reloads |
| Client-side language  | TypeScript                   | Kanban drag-and-drop and small UI helpers |
| JS/TS package manager | pnpm                         | Frontend dependencies and build tools |
| Styling               | SCSS + Open Props            | Design tokens, layouts, components, responsive design |
| Optional real-time    | Django Channels + WebSockets | Live task updates between users |

## Where each technology is used

### Django

Main backend framework. Handles area / employee / task management, task
assignment, status updates, report generation, form validation, user
authentication, and server-side rendering with templates.

### Python

Implements the business logic and demonstrates the project's
[multi-paradigm approach](paradigms.md):

- **OOP** through Django models and classes.
- **Functional** through filters, calculations, and reports.
- **Structured** through views, validations, and workflows.

### uv

Manages the Python environment and dependencies: virtual environment creation,
dependency installation and synchronization, and project execution commands.

### PostgreSQL

The relational database. Stores areas, employees, tasks, priorities, statuses,
dates and deadlines, completion records, and data used for reports.

### Django Templates

Render the user interface: dashboard, areas page, employees page, tasks page,
Kanban board, and reports page. See [Features → Main screens](features.md#main-screens).

### htmx

Adds dynamic behavior while keeping the application server-rendered:

- Updating task status without reloading the full page.
- Filtering tasks by area, employee, status, or priority.
- Loading report data dynamically.
- Refreshing task cards or page sections.
- Updating dashboard counters.

### TypeScript

Used only for client-side interactions that are difficult with htmx alone:
Kanban drag-and-drop, small UI helpers, confirmation dialogs, optional chart
interactions, and frontend utilities.

### pnpm

Manages frontend dependencies: TypeScript packages, build tools, CSS/SCSS
tooling, and optional frontend libraries.

### SCSS + Open Props

Styling via reusable design tokens: colors, spacing, typography, layouts,
buttons, cards, forms, Kanban board design, and responsive design.

### Django Channels + WebSockets (optional)

Only used if the system needs real-time updates between multiple users — e.g.
user A updates a task status and user B sees it without refreshing. Considered
an optional improvement beyond the initial scope.

## Recommended development scope

Core version:

```text
Django + PostgreSQL + Django Templates + htmx + TypeScript + SCSS
```

Optional advanced version adds:

```text
Django Channels + WebSockets
```
