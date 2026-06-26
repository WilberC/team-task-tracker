# Implementation Plan

[← Back to docs](../../README.md)

This is the phased plan to build Team Task Tracker. Each phase is a separate
file with **checkbox task lists** — tick items off as they are completed:

```markdown
- [ ] not done
- [x] done
```

Phases are ordered so each builds on the previous one. **Part 2 (the workshop)
is the priority**, so Part 1 (front desk) is kept to the minimum needed to
generate job orders — see [Domain](../domain.md).

## Phases

| # | Phase | Goal | Status |
| - | ----- | ---- | ------ |
| 0 | [Project setup & tooling](phase-0-setup.md) | Repo, Django, PostgreSQL, `src/` layout, frontend tooling | ✅ Done |
| 1 | [People & organization](phase-1-people.md) | Areas, employees, teams | ✅ Done |
| 2 | [Front desk (minimal)](phase-2-front-desk.md) | Clients, vehicles, service orders (Part 1) | ✅ Done |
| 3 | [Job orders](phase-3-job-orders.md) | Workshop hub for interned vehicles (Part 2) | ✅ Done |
| 4 | [Tasks & subtasks](phase-4-tasks.md) | The core: assignment, lifecycle, progress roll-up (Part 2) | ✅ Done |
| 5 | [Kanban board & htmx UI](phase-5-kanban-ui.md) | Drag-and-drop, inline updates, clear UX | ✅ Done |
| 6 | [Client status view](phase-6-client-view.md) | Public, read-only vehicle status | ✅ Done |
| 7 | [Dashboard & reports](phase-7-dashboard-reports.md) | Summary screen and the five reports | ✅ Done |
| 8 | [User roles & permissions](phase-8-user-roles-permissions.md) | Internal access control and role-gated workflows | ✅ Done |
| 9 | [Quality & deployment](phase-9-quality-deploy.md) | Tests, accessibility, performance, deploy | ☐ Not started |

Update the **Status** column as phases progress (e.g. ☐ → 🔄 In progress → ✅ Done).

## Conventions

These apply to every phase:

- **Modules** follow the [Architecture](../architecture.md): each lives under
  `src/<module>` with an explicit app config and an app-qualified `label`.
- **Code by paradigm** (see [Paradigms](../paradigms.md)):
  - `models.py` — entities (OOP)
  - `selectors.py` — read queries / report helpers (functional)
  - `services.py` — write orchestration (structured)
  - `views.py` — request handling
- **Templates** are app-qualified: `src/<module>/templates/<module>/...`.
- **Every feature ships with tests** in `src/<module>/tests/`.
- **UX is non-negotiable**: every screen follows the
  [UX & UI Principles](../ux-principles.md) — plain language, clear status,
  mobile-friendly, accessible.

## Definition of done (per feature)

- [ ] Models + migrations created
- [ ] Admin registered (for internal data entry)
- [ ] Views, URLs, and templates implemented
- [ ] Validation and error messages are clear and in plain language
- [ ] Tests written and passing
- [ ] Screen reviewed against the UX principles
