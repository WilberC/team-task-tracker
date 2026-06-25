# Phase 8 — User roles & permissions

[← Back to plan](README.md)

**Goal:** protect internal screens with clear workshop roles while keeping the
client status page public, read-only, and token-based.

**Depends on:** [Phase 7](phase-7-dashboard-reports.md).

**Reference:** [Features](../features.md), [UX principles](../ux-principles.md).

## Principles

- [ ] Use Django authentication for internal users.
- [ ] Use Django groups/permissions for role assignment.
- [ ] Keep `/status/<token>/` public and read-only for clients.
- [ ] Do not redirect the root landing page directly to login.
- [ ] Internal pages require login and fail closed when a user lacks permission.
- [ ] Permission errors use plain language and never expose hidden data.
- [ ] Templates hide actions the current role cannot perform.
- [ ] Views enforce permissions even if a hidden button URL is called directly.

## Roles

### Administrator

Can configure and operate the whole system.

- [ ] Manage users, groups, and role assignments.
- [ ] Access Django admin.
- [ ] Create, edit, deactivate, and view all operational records.
- [ ] Override task assignments and status when needed.
- [ ] Access dashboard and all reports.

### Front desk

Handles reception data and the minimum Part 1 workflow.

- [ ] Create and update clients.
- [ ] Create and update vehicles.
- [ ] Create and update service orders.
- [ ] View job orders generated from service orders.
- [ ] Cannot assign workshop tasks.
- [ ] Cannot close, deliver, or cancel job orders.
- [ ] Cannot access user/role management.

### Service advisor

Owns the client-facing service workflow and handoff to the workshop.

- [ ] Create and update clients, vehicles, and service orders.
- [ ] Approve service orders and generate job orders.
- [ ] View job orders, tasks, and client status links.
- [ ] Share the client status link.
- [ ] Cannot reassign mechanics unless also granted supervisor access.
- [ ] Cannot manage users or roles.

### Workshop supervisor

Runs daily workshop execution.

- [ ] View all job orders and tasks.
- [ ] Create top-level tasks and subtasks.
- [ ] Assign and reassign tasks to mechanics or teams.
- [ ] Update any task status.
- [ ] Cancel tasks with confirmation.
- [ ] Close job orders and mark vehicles delivered.
- [ ] Access Kanban, dashboard, and reports.
- [ ] Cannot manage users or roles.

### Mechanic

Works assigned tasks with minimal operational access.

- [ ] View own assigned tasks.
- [ ] View tasks assigned to their team.
- [ ] View the job order context for assigned work.
- [ ] Update status for assigned tasks.
- [ ] Add or edit subtasks under assigned parent tasks.
- [ ] Cannot view unrelated tasks by default.
- [ ] Cannot reassign tasks to other people.
- [ ] Cannot cancel tasks, close job orders, or deliver vehicles.
- [ ] Cannot access client, vehicle, or service-order editing screens.

### Manager / reports viewer

Read-only operational visibility.

- [ ] View dashboard.
- [ ] View all reports.
- [ ] View job orders and tasks.
- [ ] Cannot create, edit, cancel, close, deliver, or assign work.
- [ ] Cannot manage users or roles.

### Client

No internal account is required.

- [ ] Open only the public status link for their job order.
- [ ] See vehicle plate, make, model, friendly status, jobs, and progress.
- [ ] Cannot see costs, advisors, mechanics, internal notes, other clients, or admin links.
- [ ] Cannot mutate data.

## Permission matrix

| Capability | Admin | Front desk | Advisor | Supervisor | Mechanic | Reports viewer | Client token |
| ---------- | ----- | ---------- | ------- | ---------- | -------- | -------------- | ------------ |
| Manage users and roles | ✅ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ |
| Access Django admin | ✅ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ |
| Create/edit clients | ✅ | ✅ | ✅ | View only | ⛔ | View only | ⛔ |
| Create/edit vehicles | ✅ | ✅ | ✅ | View only | ⛔ | View only | ⛔ |
| Create/edit service orders | ✅ | ✅ | ✅ | View only | ⛔ | View only | ⛔ |
| Approve service order / generate job order | ✅ | Optional | ✅ | ⛔ | ⛔ | ⛔ | ⛔ |
| View job orders | ✅ | Related only | ✅ | ✅ | Assigned only | ✅ | Scoped status only |
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

- [ ] Define role names and permission constants in a dedicated access module.
- [ ] Add a management command or data migration to create the default groups.
- [ ] Map Django model permissions and custom permissions to each group.
- [ ] Add login and logout routes/templates using the project design system.
- [ ] Add `login_required` or permission mixins to every internal view.
- [ ] Add object-level checks for mechanic access to assigned tasks/team tasks.
- [ ] Add object-level checks for advisor/front-desk access to related service data.
- [ ] Keep the client token view outside login requirements.
- [ ] Add template helpers or context flags for role-aware actions.
- [ ] Hide unauthorized navigation items and buttons.
- [ ] Return plain-language 403 pages for unauthorized internal access.
- [ ] Add tests for every role and key route/action.

## UX requirements

- [ ] Root page remains a normal project entry screen, not a forced login redirect.
- [ ] Unauthenticated access to internal modules redirects to login with a next URL.
- [ ] After login, users land on the requested page or a role-appropriate dashboard.
- [ ] Unauthorized actions show a short explanation and a safe next action.
- [ ] Buttons and navigation reflect what the role can actually do.
- [ ] Mobile navigation remains usable when items are hidden by role.

## Security checks

- [ ] Direct POSTs to protected actions are denied without the right permission.
- [ ] Mechanic users cannot access unrelated task detail pages.
- [ ] Reports users cannot mutate records through direct URLs.
- [ ] Front desk users cannot close job orders through direct URLs.
- [ ] Public token URLs cannot expose internal staff/client/service-order data.
- [ ] Existing client token tests still pass.

## Definition of done

- [ ] Internal screens are role-gated.
- [ ] Each role can perform only the actions listed in the matrix.
- [ ] Public client status remains accessible without login.
- [ ] Tests cover role permissions, object-level access, and direct URL attempts.
- [ ] Reviewed against the [UX principles](../ux-principles.md).
