# Phase 4 — Tasks & subtasks

[← Back to plan](README.md)

**Goal:** the core of the system. Top-level tasks (jobs) under a job order,
split into subtasks, each assigned to a mechanic or team, tracked by status,
with progress rolled up.

**Depends on:** [Phase 3](phase-3-job-orders.md).

**Entities:** [Task](../data-model.md#task). See
[Subtasks](../data-model.md#subtasks),
[Assignment](../data-model.md#assignment-mechanic-or-team), and the
[task lifecycle](../workflows.md#task-lifecycle).

## Tasks module (`src/tasks`)

- [ ] Scaffold module
- [ ] `Task` model with all fields:
  - [ ] `job_order` FK (top-level only)
  - [ ] `parent_task` self-FK (nullable, for subtasks)
  - [ ] `area` FK
  - [ ] `assigned_employee` FK (nullable) and `assigned_team` FK (nullable)
  - [ ] `priority` enum (Low / Medium / High / Critical)
  - [ ] `status` enum (Pending / In progress / Completed / Overdue / Cancelled)
  - [ ] `start_date`, `due_date`, `completion_date`
- [ ] Migration → confirm table `tasks_task`
- [ ] Admin registration

## Model rules & validation

- [ ] Top-level task **must** have `job_order`; subtask **must** have `parent_task` (and no own `job_order`)
- [ ] Enforce **one level deep**: a subtask cannot be a parent
- [ ] Enforce assignment: exactly one of `assigned_employee` / `assigned_team` is set
- [ ] Subtask `area` defaults to the parent's area
- [ ] Validation errors are plain-language (see [UX](../ux-principles.md))
- [ ] Tests for every rule above

## Services (write side, structured)

- [ ] `create_top_level_task(job_order, ...)` — status starts as Pending
- [ ] `create_subtask(parent_task, ...)`
- [ ] `assign_task(task, employee_or_team)`
- [ ] `update_status(task, new_status)` — sets `completion_date` on Completed
- [ ] `cancel_task(task)`

## Lifecycle & overdue

- [ ] Implement the [status transitions](../workflows.md#task-lifecycle)
- [ ] Mark tasks **Overdue** when `due_date` passes and not completed (management command / scheduled job)
- [ ] Tests for transitions and overdue marking

## Progress roll-up

- [ ] `selectors.py`: subtask counts per parent (e.g. "2 of 3 done")
- [ ] Parent → Completed only when all subtasks Completed/Cancelled
- [ ] Flag parent **at risk** if any subtask Overdue
- [ ] Propagate to job order status ([Phase 3](phase-3-job-orders.md#status-derivation))
- [ ] Tests for roll-up logic (see [diagram](../workflows.md#subtask-progress-roll-up))

## Screens (basic, enhanced in Phase 5)

- [ ] Add top-level task to a job order
- [ ] Add subtasks to a task; show progress indicator
- [ ] Task detail with assignment, status, dates
- [ ] Task list with filters: job order, area, mechanic/team, status, priority, due date
- [ ] Templates (`tasks/...`)

## Definition of done

- [ ] A job order can hold jobs, each split into assigned, status-tracked subtasks
- [ ] Parent and job order progress update automatically from subtasks
- [ ] Overdue tasks are flagged
- [ ] Tests passing
