# Phase 1 — People & organization

[← Back to plan](README.md)

**Goal:** register the work areas, employees (mechanics/advisors), and teams
that tasks will later be assigned to.

**Depends on:** [Phase 0](phase-0-setup.md).

**Entities:** [Area](../data-model.md#area), [Employee](../data-model.md#employee),
[Team](../data-model.md#team).

## Areas module (`src/areas`)

- [x] Scaffold module: `uv run python manage.py startmodule areas`
- [x] `Area` model (`name`, `description`, `active`) with label `areas`
- [x] Migration → confirm table `areas_area`
- [x] Admin registration
- [x] List, create, edit views + app-qualified templates (`areas/...`)
- [x] Tests: model + views
- [x] Seed example areas (Mechanical, Bodywork, Paint, Electrical)

## Employees module (`src/employees`)

- [x] Scaffold module
- [x] `Employee` model (`full_name`, `email`, `area` FK, `position`, `active`)
- [x] Migration → confirm table `employees_employee`
- [x] Admin registration
- [x] List, create, edit views + templates
- [x] Selector: active employees by area (for assignment dropdowns)
- [x] Tests: model + views

## Teams module (`src/teams`)

- [x] Scaffold module
- [x] `Team` model (`name`, `area` FK, `members` M2M → Employee, `active`)
- [x] Migration → confirm table `teams_team`
- [x] Admin registration (inline members)
- [x] List, create, edit views + templates
- [x] Selector: active teams by area
- [x] Tests: model + views

## Definition of done

- [x] Admin can register areas, employees, and teams via the UI
- [x] Inactive areas/employees/teams are excluded from assignment selectors
- [x] All screens follow the [UX principles](../ux-principles.md)
- [x] Tests passing
