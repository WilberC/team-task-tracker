# Overview

[← Back to README](../README.md)

## Project summary

**Team Task Tracker** is a web system for a **mechanic workshop** ("taller
mecánico"). It tracks the work done on each interned vehicle — from the service
order negotiated with the client, to the job order, down to the individual
tasks each mechanic or team performs — so the shop always knows who is doing
what and the client can follow their vehicle's progress.

The work splits into two parts (see [Domain](domain.md)):

- **Part 1 — Front desk:** an advisor negotiates the work and records a
  **service order**. Kept simple for the first version.
- **Part 2 — Workshop (the priority):** the service order generates a **job
  order**; the vehicle is interned and the work is broken into tasks and
  subtasks, each assigned and tracked by status.

The system is designed for **non-technical users**, so a clear, simple, and
friendly interface is a core requirement, not an afterthought — see
[UX & UI Principles](ux-principles.md). A job can be **divided into subtasks**
so large pieces of work stay manageable.

## The problem

In a workshop, work is often coordinated informally through messages or word of
mouth. This causes:

- Lack of clarity about who is working on which vehicle and task.
- Difficulty tracking pending or delayed work.
- Poor visibility of each mechanic's or team's workload.
- No clear way for the client to know their vehicle's status.
- No reliable reports about productivity or on-time completion.

## Objective

Develop a web application that allows the **registration, assignment,
tracking, and reporting** of workshop work — organized by job order, area, and
mechanic/team — with a read-only status view for clients.

## Scope

### In scope (Part 2 — the focus)

- Job orders for interned vehicles
- Task creation under a job order
- Splitting a job into subtasks
- Assigning tasks to a mechanic or a team
- Task status updates and progress roll-up
- Task filters
- Read-only client status view
- Basic reports
- Areas, employees, and teams

### In scope (Part 1 — minimal for now)

- Clients and vehicles
- Service orders that generate a job order

### Out of scope

- Payroll
- Detailed billing / invoicing and parts inventory
- Real-time chat
- Email notifications
- Complex user permissions
- Integration with external tools

## Expected result

The system should help the workshop organize its work through better task
assignment, progress tracking, and basic reporting. It should give a clear view of:

- Who is working on each vehicle and task.
- Which tasks are pending or overdue.
- Which areas are completing more work.
- Which mechanics or teams have more assigned work.
- Whether work is being completed on time.
- The current status of each vehicle, visible to its client.

## Related documents

- [Domain](domain.md) — the auto repair workshop context and the two parts.
- [Features](features.md) — what the system does in detail.
- [Workflows](workflows.md) — how work moves through the shop.
- [Reports](reports.md) — the reporting outputs.
