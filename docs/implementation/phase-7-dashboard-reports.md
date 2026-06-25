# Phase 7 — Dashboard & reports

[← Back to plan](README.md)

**Goal:** give the shop a clear overview and the five reports, built as
read-only functional aggregations.

**Depends on:** [Phase 4](phase-4-tasks.md).

**Reference:** [Reports](../reports.md),
[Paradigms → Functional](../paradigms.md#functional-programming).

## Dashboard module (`src/dashboard`)

- [x] Scaffold module
- [x] Summary cards: vehicles in shop, tasks by status, overdue/critical highlighted
- [x] "What each mechanic/team is doing right now" panel
- [x] htmx-refreshed counters
- [x] Templates (`dashboard/...`)

## Reports module (`src/reports`)

- [x] Scaffold module
- [x] Report 1 — [Tasks by status](../reports.md#1-tasks-by-status)
- [x] Report 2 — [Overdue tasks](../reports.md#2-overdue-tasks)
- [x] Report 3 — [Workload by mechanic or team](../reports.md#3-workload-by-mechanic-or-team)
- [x] Report 4 — [Productivity by area](../reports.md#4-productivity-by-area) (date range)
- [x] Report 5 — [Deadline compliance](../reports.md#5-deadline-compliance) (on time vs late %)
- [x] Implement each as a pure `selectors.py` function (functional, testable)
- [x] Reports page: charts/big numbers first, each with a one-line plain explanation
- [x] Tests for each report's aggregation

## Definition of done

- [x] Dashboard shows an accurate, at-a-glance picture of the shop
- [x] All five reports return correct numbers (verified by tests)
- [x] Reports are visual and understandable without explanation
