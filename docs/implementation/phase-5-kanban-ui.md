# Phase 5 — Kanban board & htmx UI

[← Back to plan](README.md)

**Goal:** make the day-to-day task work fast and intuitive for non-technical
users — a drag-and-drop Kanban board and inline updates with no jarring
reloads.

**Depends on:** [Phase 4](phase-4-tasks.md).

**Reference:** [UX & UI Principles](../ux-principles.md),
[Tech Stack](../tech-stack.md).

## Kanban board

- [ ] Board view with a column per status (Pending / In progress / Completed / Overdue / Cancelled)
- [ ] Task cards show title, assignee (mechanic/team), priority, due date
- [ ] Status shown with **color *and* label/icon** (not color alone)
- [ ] TypeScript drag-and-drop (`src/tasks/assets/ts/kanban.ts`)
- [ ] Dropping a card calls the status-update endpoint (htmx) and persists
- [ ] Optimistic UI with rollback on error

## htmx interactions

- [ ] Update task status inline without full page reload
- [ ] Filter tasks (job order, area, mechanic/team, status, priority, due date) via htmx
- [ ] Add/edit subtasks inline; refresh the parent progress indicator
- [ ] Inline form validation with plain-language errors

## UX polish

- [ ] One clear primary action per screen (e.g. **+ New task**)
- [ ] Empty states that explain what to do first
- [ ] Confirmation dialogs for destructive/irreversible actions
- [ ] Smart defaults (status = Pending auto-set; "My tasks" / "Due this week" filters)
- [ ] List view alternative to the board

## Definition of done

- [ ] A mechanic can drag a card between columns and the status persists
- [ ] Filters and subtask edits update inline without a full reload
- [ ] Keyboard and screen-reader accessible; works on mobile
- [ ] Reviewed against the [UX principles](../ux-principles.md)
