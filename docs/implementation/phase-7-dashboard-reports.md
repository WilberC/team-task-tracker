# Phase 7 — Dashboard & reports

[← Back to plan](README.md)

**Goal:** give the shop a clear overview and the five reports, built as
read-only functional aggregations.

**Depends on:** [Phase 4](phase-4-tasks.md).

**Reference:** [Reports](../reports.md),
[Paradigms → Functional](../paradigms.md#functional-programming).

## Dashboard module (`src/dashboard`)

- [ ] Scaffold module
- [ ] Summary cards: vehicles in shop, tasks by status, overdue/critical highlighted
- [ ] "What each mechanic/team is doing right now" panel
- [ ] htmx-refreshed counters
- [ ] Templates (`dashboard/...`)

## Reports module (`src/reports`)

- [ ] Scaffold module
- [ ] Report 1 — [Tasks by status](../reports.md#1-tasks-by-status)
- [ ] Report 2 — [Overdue tasks](../reports.md#2-overdue-tasks)
- [ ] Report 3 — [Workload by mechanic or team](../reports.md#3-workload-by-mechanic-or-team)
- [ ] Report 4 — [Productivity by area](../reports.md#4-productivity-by-area) (date range)
- [ ] Report 5 — [Deadline compliance](../reports.md#5-deadline-compliance) (on time vs late %)
- [ ] Implement each as a pure `selectors.py` function (functional, testable)
- [ ] Reports page: charts/big numbers first, each with a one-line plain explanation
- [ ] Tests for each report's aggregation

## Definition of done

- [ ] Dashboard shows an accurate, at-a-glance picture of the shop
- [ ] All five reports return correct numbers (verified by tests)
- [ ] Reports are visual and understandable without explanation
