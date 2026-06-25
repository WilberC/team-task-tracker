# Phase 1 — People & organization

[← Back to plan](README.md)

**Goal:** register the work areas, employees (mechanics/advisors), and teams
that tasks will later be assigned to.

**Depends on:** [Phase 0](phase-0-setup.md).

**Entities:** [Area](../data-model.md#area), [Employee](../data-model.md#employee),
[Team](../data-model.md#team).

## Areas module (`src/areas`)

- [ ] Scaffold module: `uv run python manage.py startmodule areas`
- [ ] `Area` model (`name`, `description`, `active`) with label `areas`
- [ ] Migration → confirm table `areas_area`
- [ ] Admin registration
- [ ] List, create, edit views + app-qualified templates (`areas/...`)
- [ ] Tests: model + views
- [ ] Seed example areas (Mechanical, Bodywork, Paint, Electrical)

## Employees module (`src/employees`)

- [ ] Scaffold module
- [ ] `Employee` model (`full_name`, `email`, `area` FK, `position`, `active`)
- [ ] Migration → confirm table `employees_employee`
- [ ] Admin registration
- [ ] List, create, edit views + templates
- [ ] Selector: active employees by area (for assignment dropdowns)
- [ ] Tests: model + views

## Teams module (`src/teams`)

- [ ] Scaffold module
- [ ] `Team` model (`name`, `area` FK, `members` M2M → Employee, `active`)
- [ ] Migration → confirm table `teams_team`
- [ ] Admin registration (inline members)
- [ ] List, create, edit views + templates
- [ ] Selector: active teams by area
- [ ] Tests: model + views

## Definition of done

- [ ] Admin can register areas, employees, and teams via the UI
- [ ] Inactive areas/employees/teams are excluded from assignment selectors
- [ ] All screens follow the [UX principles](../ux-principles.md)
- [ ] Tests passing
