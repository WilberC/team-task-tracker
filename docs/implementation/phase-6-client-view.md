# Phase 6 — Client status view

[← Back to plan](README.md)

**Goal:** let a client **join and see the status of their vehicle** through a
public, read-only page — clear and jargon-free.

**Depends on:** [Phase 4](phase-4-tasks.md) (so there is progress to show).

**Reference:** [Features → Client status view](../features.md#client-status-view),
[UX principles](../ux-principles.md).

## Access

- [ ] Decide the access method (e.g. a per-job-order shareable link/token — no account needed)
- [ ] Generate a unique, hard-to-guess token per job order
- [ ] Public route that resolves the token to a job order (read-only)
- [ ] No internal data leaks (no costs, internal notes, other clients)

## The status page

- [ ] Show vehicle (plate, make, model) and a friendly overall status
- [ ] Show the jobs and a simple progress summary (e.g. "Diagnostic done, brake repair in progress")
- [ ] Use plain language and status color + label (no internal codes)
- [ ] `selectors.py`: client-safe view of a job order's progress
- [ ] Mobile-first layout (clients will mostly use phones)

## Optional

- [ ] Live updates via htmx polling or Channels (see [Tech Stack](../tech-stack.md))

## Definition of done

- [ ] A client opens their link and sees the current vehicle status with no login
- [ ] The page exposes only client-appropriate information
- [ ] Tests cover token resolution and that internal fields are not exposed
- [ ] Reviewed against the [UX principles](../ux-principles.md)
