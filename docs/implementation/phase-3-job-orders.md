# Phase 3 — Job orders

[← Back to plan](README.md)

**Goal:** the workshop hub. A service order **generates a job order** (the job
order id); the vehicle is interned and tracked until delivery.

**Depends on:** [Phase 2](phase-2-front-desk.md).

**Entities:** [Job Order](../data-model.md#job-order). See
[Domain → Part 2](../domain.md#part-2--workshop-execution-the-focus) and the
[workshop flow](../workflows.md#workshop-flow-service-order--job-order--tasks).

## Workshop module (`src/workshop`)

- [x] Scaffold module
- [x] `JobOrder` model (`service_order` FK, `vehicle` FK, `status`, `interned_at`, `closed_at`)
- [x] Status enum (Open / In progress / Done / Delivered)
- [x] Migration → confirm table `workshop_joborder`
- [x] Admin registration

## Generate job order from service order

- [x] `services.py`: `generate_job_order(service_order)` — creates the job order on approval
- [x] Guard: a service order generates **one** job order (no duplicates)
- [x] Wire the "Approve service order" action ([Phase 2](phase-2-front-desk.md)) to call it
- [x] Record `interned_at` when the vehicle is checked in

## Job order screens

- [x] Job orders list (open / in-progress vehicles) with clear status labels
- [x] Job order detail page: vehicle, client, status, and its top-level tasks (tasks added in [Phase 4](phase-4-tasks.md))
- [x] "Close job order" / "Mark delivered" actions with confirmation
- [x] `selectors.py`: open job orders, job order with tasks
- [x] Templates (`workshop/...`)

## Status derivation

- [ ] Job order status reflects its tasks (Open → In progress → Done) — finalize the roll-up in [Phase 4](phase-4-tasks.md#progress-roll-up)
- [x] Tests: generation guard, status transitions

## Definition of done

- [x] Approving a service order creates exactly one job order with an id
- [x] Staff can see all vehicles currently in the shop and open any job order
- [x] Tests passing
