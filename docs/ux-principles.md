# UX & UI Principles

[← Back to README](../README.md)

> **Audience first:** this system is built for **non-technical people** —
> administrators, area leads, and employees who are not developers and may not
> use software tools every day. Every screen must be understandable without
> training, a manual, or jargon. When a design choice trades power for
> clarity, **choose clarity.**

## Who uses this

| User | Goal | Comfort with software |
| ---- | ---- | --------------------- |
| Administrator / area lead | Set up areas and people, assign work, check reports | Low–medium |
| Employee | See my tasks, update progress, mark things done | Low |

Assume the user is busy, on a normal laptop or phone, and wants to get in, do
one thing, and get out.

## Guiding principles

1. **Plain language, not jargon.** Use everyday words: "Who's responsible?"
   instead of "Assignee", "Due" instead of "Deadline (UTC)". Never show
   internal terms like IDs, enums, or status codes.
2. **One primary action per screen.** Each page has one obvious thing to do,
   shown as a single prominent button (e.g. **+ New task**). Secondary actions
   are visually quieter.
3. **Show status with color *and* words.** Never rely on color alone (for
   color-blind users): pair it with a label and/or icon — 🟢 Completed,
   🔵 In progress, 🟡 Pending, 🔴 Overdue, ⚪ Cancelled.
4. **Guide, don't block.** Validate forms inline, explain errors in plain
   language ("Please pick a due date"), and never lose what the user typed.
5. **Confirm destructive or irreversible actions** with a clear question, and
   keep everything else one click.
6. **Empty states teach.** A page with no data explains what it's for and how
   to add the first item, instead of showing a blank screen.
7. **Mobile-friendly and accessible.** Responsive layout, large tap targets,
   readable font sizes, keyboard navigation, and proper labels for screen
   readers.

## Applying it to key screens

### Dashboard

- Big, friendly summary cards: **Total**, **Pending**, **In progress**,
  **Completed**, **Overdue** — each a number with a clear label and color.
- Highlight what needs attention first (overdue and critical tasks).

### Tasks page

- A **Kanban board** with columns per status is the default view, because
  dragging a card from "In progress" to "Completed" is intuitive for everyone.
- A simple **list view** with filters is available for those who prefer it.
- Filters use plain labels and sensible defaults (e.g. "My tasks", "Due this
  week").

### Creating / editing a task

- Short form, grouped logically: **What** (title, description), **Who** (area,
  responsible person), **When** (due date), **How urgent** (priority).
- Smart defaults: status starts as Pending automatically — the user never
  picks it.

### Subtasks

- Splitting a task is a single **"Break into subtasks"** action on the task.
- Subtasks appear as a simple checklist under the parent with a clear
  **"2 of 3 done"** progress indicator and progress bar.
- Kept **one level deep** on purpose — no confusing nested trees. See
  [Features → Subtasks](features.md#subtasks).

### Reports

- Visual first: charts and big numbers over dense tables.
- Each report has a one-line plain-language explanation of what it shows and
  why it matters. See [Reports](reports.md).

## How the stack supports this

- **htmx** keeps interactions fast and inline (update a status, filter a list)
  without jarring full-page reloads.
- **TypeScript** powers the drag-and-drop Kanban that makes status changes feel
  natural.
- **SCSS + Open Props** provide consistent spacing, color, and typography
  tokens so the whole app feels coherent and calm.

See [Tech Stack](tech-stack.md) for details.
