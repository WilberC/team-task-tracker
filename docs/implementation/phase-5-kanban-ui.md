# Phase 5 — Kanban board & htmx UI

[← Back to plan](README.md)

**Goal:** make the day-to-day task work fast and intuitive for non-technical
users — a drag-and-drop Kanban board and inline updates with no jarring
reloads.

**Depends on:** [Phase 4](phase-4-tasks.md).

**Reference:** [UX & UI Principles](../ux-principles.md),
[Tech Stack](../tech-stack.md).

## Kanban board

- [x] Board view with a column per status (Pending / In progress / Completed / Overdue / Cancelled)
- [x] Task cards show title, assignee (mechanic/team), priority, due date
- [x] Status shown with **color *and* label/icon** (not color alone)
- [x] TypeScript drag-and-drop (`src/tasks/assets/ts/kanban.ts`)
- [x] Dropping a card calls the status-update endpoint (htmx) and persists
- [x] Optimistic UI with rollback on error

## htmx interactions

- [x] Update task status inline without full page reload
- [x] Filter tasks (job order, area, mechanic/team, status, priority, due date) via htmx
- [x] Add/edit subtasks inline; refresh the parent progress indicator
- [x] Inline form validation with plain-language errors

## UX polish

- [x] One clear primary action per screen (e.g. **+ New task**)
- [x] Empty states that explain what to do first
- [x] Confirmation dialogs for destructive/irreversible actions
- [x] Smart defaults (status = Pending auto-set; "My tasks" / "Due this week" filters)
- [x] List view alternative to the board

## Definition of done

- [x] A mechanic can drag a card between columns and the status persists
- [x] Filters and subtask edits update inline without a full reload
- [x] Keyboard and screen-reader accessible; works on mobile
- [x] Reviewed against the [UX principles](../ux-principles.md)
