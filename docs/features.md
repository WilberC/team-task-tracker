# Features

[← Back to README](../README.md)

This document describes the functional building blocks of the system, which
serves an [auto repair workshop](domain.md). For how these pieces interact over
time, see [Workflows](workflows.md); for the underlying entities, see the
[Data Model](data-model.md).

The two parts of the business:

- **Front desk (Part 1, kept simple):** clients, vehicles, and service orders.
- **Workshop (Part 2, the focus):** job orders and the task hierarchy.

## Front desk (Part 1)

> Minimal for the first version — see [Domain](domain.md).

### Clients and vehicles

Register clients and the vehicles they bring in (plate, make, model, year). A
client can later **follow their vehicle's status online** (see
[client status view](#client-status-view)).

### Service orders

An advisor records the work negotiated with the client as a **service order**.
Approving a service order **generates a job order** to start the workshop work.

## Workshop (Part 2)

### Job orders

A **job order** represents the work on one interned (checked-in) vehicle and
carries the **job order id**. From a job order, staff:

- See the vehicle and client.
- Add the **jobs to do** as top-level tasks (the first being the **diagnostic**,
  assigned to one mechanic).
- Track overall status until the vehicle is delivered.

Every **top-level task belongs to a job order**.

## Task management

Tasks are the units of work inside a job order. Each task has:

- Title
- Description
- Job order (on top-level tasks) / parent task (on subtasks)
- Area
- Responsible **mechanic or team** (see [assignment](#assignment-mechanic-or-team))
- Priority
- Status
- Start date
- Due date
- Completion date

### Assignment: mechanic or team

Each task is assigned to whoever does the work — **normally the same mechanic**
handling the job order, but it can be **any other mechanic or a team**. This is
how the shop knows who is doing what at any moment.

### Subtasks

A job (top-level task) can be **broken into smaller subtasks** so the work feels
manageable. For example, *Brake repair* can be split into "Inspect pads",
"Replace discs", and "Road test".

- Each subtask is a normal task: it has its own responsible mechanic/team,
  priority, status, and due date.
- A parent task shows a simple **progress indicator** (e.g. "2 of 3 done") so
  anyone can see how far along it is at a glance.
- To keep things clear for non-technical users, subtasks go **only one level
  deep** — a subtask cannot be split again. See the
  [data model](data-model.md#subtasks) for the underlying rules.

### Priority

Priority helps identify which tasks require more attention.

| Priority | Meaning |
| -------- | ------- |
| Low      | Can wait; no time pressure |
| Medium   | Normal day-to-day work |
| High     | Should be handled soon |
| Critical | Needs immediate attention |

### Status

Status tracks the progress of each task. See the
[task lifecycle diagram](workflows.md#task-lifecycle) for valid transitions.

| Status      | Meaning |
| ----------- | ------- |
| Pending     | Created but not started |
| In progress | Being worked on |
| Completed   | Finished |
| Overdue     | Past its due date and not completed |
| Cancelled   | No longer needed |

## Task filtering

Users can view tasks using filters such as:

- Job order
- Area
- Mechanic or team
- Status
- Priority
- Due date
- Completed tasks
- Overdue tasks

## Client status view

The client can **join and see the status of their vehicle** without logging into
the internal system — a simple, read-only page showing the job order progress
(e.g. "Diagnostic done, brake repair in progress"). It must be especially clear
and jargon-free; see [UX & UI Principles](ux-principles.md).

## Main screens

| Screen           | Purpose |
| ---------------- | ------- |
| **Dashboard**    | General summary: vehicles in the shop, tasks by status, what each mechanic is doing |
| **Job orders page** | View interned vehicles and the work on each (the workshop hub) |
| **Tasks page**   | Create, update, filter, and view tasks (Kanban + list) |
| **Service orders page** | Front desk: negotiated work (Part 1, simple) |
| **Clients & vehicles** | Register and view clients and their vehicles |
| **Areas / Employees / Teams** | Register and view areas, mechanics, and teams |
| **Reports page** | Task reports and basic statistics ([details](reports.md)) |
| **Client status view** | Public, read-only vehicle status for the client |
