# Phase 8 — User roles & permissions

[← Back to plan](README.md)

**Goal:** protect internal screens with clear workshop roles while keeping the
client status page public, read-only, and token-based.

**Depends on:** [Phase 7](phase-7-dashboard-reports.md).

**Reference:** [Features](../features.md), [UX principles](../ux-principles.md).

## Principles

- [x] Use Django authentication for internal users.
- [x] Use Django groups/permissions for role assignment.
- [x] Keep `/status/<token>/` public and read-only for clients.
- [x] Do not redirect the root landing page directly to login.
- [x] Internal pages require login and fail closed when a user lacks permission.
- [x] Permission errors use plain language and never expose hidden data.
- [x] Templates hide actions the current role cannot perform.
- [x] Views enforce permissions even if a hidden button URL is called directly.

## Roles

### Administrator

Can configure and operate the whole system.

- [x] Manage users, groups, and role assignments.
- [x] Access Django admin.
- [x] Create, edit, deactivate, and view all operational records.
- [x] Override task assignments and status when needed.
- [x] Access dashboard and all reports.

### Front desk

Handles reception data and the minimum Part 1 workflow.

- [x] Create and update clients.
- [x] Create and update vehicles.
- [x] Create and update service orders.
- [x] View job orders generated from service orders.
- [x] Cannot assign workshop tasks.
- [x] Cannot close, deliver, or cancel job orders.
- [x] Cannot access user/role management.

### Service advisor

Owns the client-facing service workflow and handoff to the workshop.

- [x] Create and update clients, vehicles, and service orders.
- [x] Approve service orders and generate job orders.
- [x] View job orders, tasks, and client status links.
- [x] Share the client status link.
- [x] Cannot reassign mechanics unless also granted supervisor access.
- [x] Cannot manage users or roles.

### Workshop supervisor

Runs daily workshop execution.

- [x] View all job orders and tasks.
- [x] Create top-level tasks and subtasks.
- [x] Assign and reassign tasks to mechanics or teams.
- [x] Update any task status.
- [x] Cancel tasks with confirmation.
- [x] Close job orders and mark vehicles delivered.
- [x] Access Kanban, dashboard, and reports.
- [x] Cannot manage users or roles.

### Mechanic

Works assigned tasks with minimal operational access.

- [x] View own assigned tasks.
- [x] View tasks assigned to their team.
- [x] View the job order context for assigned work.
- [x] Update status for assigned tasks.
- [x] Add or edit subtasks under assigned parent tasks.
- [x] Cannot view unrelated tasks by default.
- [x] Cannot reassign tasks to other people.
- [x] Cannot cancel tasks, close job orders, or deliver vehicles.
- [x] Cannot access client, vehicle, or service-order editing screens.

### Manager / reports viewer

Read-only operational visibility.

- [x] View dashboard.
- [x] View all reports.
- [x] View job orders and tasks.
- [x] Cannot create, edit, cancel, close, deliver, or assign work.
- [x] Cannot manage users or roles.

### Client

No internal account is required.

- [x] Open only the public status link for their job order.
- [x] See vehicle plate, make, model, friendly status, jobs, and progress.
- [x] Cannot see costs, advisors, mechanics, internal notes, other clients, or admin links.
- [x] Cannot mutate data.

## Permission matrix

| Capability | Admin | Front desk | Advisor | Supervisor | Mechanic | Reports viewer | Client token |
| ---------- | ----- | ---------- | ------- | ---------- | -------- | -------------- | ------------ |
| Manage users and roles | ✅ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ |
| Access Django admin | ✅ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ |
| Create/edit clients | ✅ | ✅ | ✅ | View only | ⛔ | View only | ⛔ |
| Create/edit vehicles | ✅ | ✅ | ✅ | View only | ⛔ | View only | ⛔ |
| Create/edit service orders | ✅ | ✅ | ✅ | View only | ⛔ | View only | ⛔ |
| Approve service order / generate job order | ✅ | Optional | ✅ | ⛔ | ⛔ | ⛔ | ⛔ |
| View job orders | ✅ | ✅ | ✅ | ✅ | Assigned only | ✅ | Scoped status only |
| Close/deliver job orders | ✅ | ⛔ | ⛔ | ✅ | ⛔ | ⛔ | ⛔ |
| Create/edit tasks | ✅ | ⛔ | View only | ✅ | Assigned subtasks only | ⛔ | ⛔ |
| Assign/reassign tasks | ✅ | ⛔ | ⛔ | ✅ | ⛔ | ⛔ | ⛔ |
| Update task status | ✅ | ⛔ | ⛔ | ✅ | Assigned only | ⛔ | ⛔ |
| Cancel tasks | ✅ | ⛔ | ⛔ | ✅ | ⛔ | ⛔ | ⛔ |
| Kanban board | ✅ | ⛔ | View only | ✅ | Assigned only | View only | ⛔ |
| Dashboard | ✅ | ⛔ | ✅ | ✅ | ⛔ | ✅ | ⛔ |
| Reports | ✅ | ⛔ | Optional | ✅ | ⛔ | ✅ | ⛔ |
| Public client status page | ✅ | ✅ | ✅ | ✅ | ⛔ | ⛔ | ✅ |

## Implementation tasks

- [x] Define role names and permission constants in a dedicated access module.
- [x] Add a management command or data migration to create the default groups.
- [x] Map Django model permissions and role permissions to each group.
- [x] Add login and logout routes/templates using the project design system.
- [x] Add `login_required` or permission mixins to every internal view.
- [x] Add object-level checks for mechanic access to assigned tasks/team tasks.
- [x] Confirm advisor/front-desk service data scope uses role-level access.
- [x] Keep the client token view outside login requirements.
- [x] Add template helpers or context flags for role-aware actions.
- [x] Hide unauthorized navigation items and buttons.
- [x] Return plain-language 403 pages for unauthorized internal access.
- [x] Add tests for every role and key route/action.

## UX requirements

- [x] Root page remains a normal project entry screen, not a forced login redirect.
- [x] Unauthenticated access to internal modules redirects to login with a next URL.
- [x] After login, users land on the requested page or a role-appropriate dashboard.
- [x] Unauthorized actions show a short explanation and a safe next action.
- [x] Buttons and navigation reflect what the role can actually do.
- [x] Mobile navigation remains usable when items are hidden by role.

## Security checks

- [x] Direct POSTs to protected actions are denied without the right permission.
- [x] Mechanic users cannot access unrelated task detail pages.
- [x] Reports users cannot mutate records through direct URLs.
- [x] Front desk users cannot close job orders through direct URLs.
- [x] Public token URLs cannot expose internal staff/client/service-order data.
- [x] Existing client token tests still pass.

## Definition of done

- [x] Internal screens are role-gated.
- [x] Each role can perform only the actions listed in the matrix.
- [x] Public client status remains accessible without login.
- [x] Tests cover role permissions, object-level access, and direct URL attempts.
- [x] Reviewed against the [UX principles](../ux-principles.md).
