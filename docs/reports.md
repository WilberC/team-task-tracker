# Reports

[← Back to README](../README.md)

The system produces five reports from task data. These are read-only
aggregations, implemented with functional-style data processing (see
[Paradigms](paradigms.md#functional-programming)) and surfaced on the Reports
page.

## 1. Tasks by status

Number of tasks grouped by status. Example:

| Status      | Count |
| ----------- | ----- |
| Pending     | 10 |
| In progress | 5 |
| Completed   | 20 |
| Overdue     | 3 |

## 2. Overdue tasks

All tasks that passed their due date and were not completed. Helps identify
delays and urgent work.

## 3. Workload by mechanic or team

How many tasks are assigned to each mechanic or team. Helps detect who is
overloaded and who has spare capacity.

## 4. Productivity by area

How many tasks each area (Mechanical, Bodywork, Paint, …) completed during a
specific period. Helps compare the performance of different areas.

## 5. Deadline compliance

The percentage of tasks completed on time versus completed late. Example:

| Outcome           | Percentage |
| ----------------- | ---------- |
| Completed on time | 80% |
| Completed late    | 20% |

## Related documents

- [Data Model](data-model.md) — the fields these reports aggregate.
- [Workflows](workflows.md) — how `completion_date` and `due_date` are set.
