# Phase 9 — Quality & deployment

[← Back to plan](README.md)

**Goal:** harden the application and ship it.

**Depends on:** all previous phases, including
[Phase 8](phase-8-user-roles-permissions.md).

## Testing

- [ ] Unit tests for models, selectors, and services across all modules
- [ ] View/integration tests for the main flows (service order → job order → tasks)
- [ ] Test the overdue-marking job and progress roll-up edge cases
- [ ] Test the client view exposes only safe data
- [ ] Set a coverage target and wire it into CI

## Accessibility & UX review

- [ ] Audit every screen against the [UX principles](../ux-principles.md)
- [ ] Color contrast, focus order, keyboard navigation, screen-reader labels
- [ ] Verify status is conveyed by color **and** text everywhere
- [ ] Mobile/responsive pass (especially the client view and Kanban)

## Performance

- [x] Add DB indexes (job_order, parent_task, status, due_date, assignees)
- [x] Eliminate N+1 queries in lists/board (`select_related` / `prefetch_related`)
- [x] Compress and cache static assets

## Security

- [x] CSRF, auth on internal screens, permissions for internal vs public routes
- [x] Client tokens are unguessable and scoped to one job order
- [x] Secrets via env vars; `DEBUG=False` in production

## Deployment

- [x] Production settings (allowed hosts, static via `collectstatic`, logging)
- [x] ASGI server (for optional Channels) and PostgreSQL provisioning
- [ ] CI pipeline: lint, test, build frontend
- [ ] Run migrations on deploy; smoke-test the live app
- [x] Document the deploy and rollback steps

## Definition of done

- [ ] All tests green in CI
- [ ] Accessibility and UX review signed off
- [ ] App deployed and reachable, with the full flow working end to end
