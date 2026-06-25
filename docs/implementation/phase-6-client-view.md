# Phase 6 — Client status view

[← Back to plan](README.md)

**Goal:** let a client **join and see the status of their vehicle** through a
public, read-only page — clear and jargon-free.

**Depends on:** [Phase 4](phase-4-tasks.md) (so there is progress to show).

**Reference:** [Features → Client status view](../features.md#client-status-view),
[UX principles](../ux-principles.md).

## Access

- [x] Decide the access method (e.g. a per-job-order shareable link/token — no account needed)
- [x] Generate a unique, hard-to-guess token per job order
- [x] Public route that resolves the token to a job order (read-only)
- [x] No internal data leaks (no costs, internal notes, other clients)

## The status page

- [x] Show vehicle (plate, make, model) and a friendly overall status
- [x] Show the jobs and a simple progress summary (e.g. "Diagnostic done, brake repair in progress")
- [x] Use plain language and status color + label (no internal codes)
- [x] `selectors.py`: client-safe view of a job order's progress
- [x] Mobile-first layout (clients will mostly use phones)

## Optional

- [ ] Live updates via htmx polling or Channels (see [Tech Stack](../tech-stack.md))

## Definition of done

- [x] A client opens their link and sees the current vehicle status with no login
- [x] The page exposes only client-appropriate information
- [x] Tests cover token resolution and that internal fields are not exposed
- [x] Reviewed against the [UX principles](../ux-principles.md)
