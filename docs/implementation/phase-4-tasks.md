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

- [x] Scaffold module
- [x] `Task` model with all fields:
  - [x] `job_order` FK (top-level only)
  - [x] `parent_task` self-FK (nullable, for subtasks)
  - [x] `area` FK
  - [x] `assigned_employee` FK (nullable) and `assigned_team` FK (nullable)
  - [x] `priority` enum (Low / Medium / High / Critical)
  - [x] `status` enum (Pending / In progress / Completed / Overdue / Cancelled)
  - [x] `start_date`, `due_date`, `completion_date`
- [x] Migration → confirm table `tasks_task`
- [x] Admin registration

## Model rules & validation

- [x] Top-level task **must** have `job_order`; subtask **must** have `parent_task` (and no own `job_order`)
- [x] Enforce **one level deep**: a subtask cannot be a parent
- [x] Enforce assignment: exactly one of `assigned_employee` / `assigned_team` is set
- [x] Subtask `area` defaults to the parent's area
- [x] Validation errors are plain-language (see [UX](../ux-principles.md))
- [x] Tests for every rule above

## Services (write side, structured)

- [x] `create_top_level_task(job_order, ...)` — status starts as Pending
- [x] `create_subtask(parent_task, ...)`
- [x] `assign_task(task, employee_or_team)`
- [x] `update_status(task, new_status)` — sets `completion_date` on Completed
- [x] `cancel_task(task)`

## Lifecycle & overdue

- [x] Implement the [status transitions](../workflows.md#task-lifecycle)
- [x] Mark tasks **Overdue** when `due_date` passes and not completed (management command / scheduled job)
- [x] Tests for transitions and overdue marking

## Progress roll-up

- [x] `selectors.py`: subtask counts per parent (e.g. "2 of 3 done")
- [x] Parent → Completed only when all subtasks Completed/Cancelled
- [x] Flag parent **at risk** if any subtask Overdue
- [x] Propagate to job order status ([Phase 3](phase-3-job-orders.md#status-derivation))
- [x] Tests for roll-up logic (see [diagram](../workflows.md#subtask-progress-roll-up))

## Screens (basic, enhanced in Phase 5)

- [x] Add top-level task to a job order
- [x] Add subtasks to a task; show progress indicator
- [x] Task detail with assignment, status, dates
- [x] Task list with filters: job order, area, mechanic/team, status, priority, due date
- [x] Templates (`tasks/...`)

## Definition of done

- [x] A job order can hold jobs, each split into assigned, status-tracked subtasks
- [x] Parent and job order progress update automatically from subtasks
- [x] Overdue tasks are flagged
- [x] Tests passing
