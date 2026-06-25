# Programming Paradigms

[← Back to README](../README.md)

The system is **multi-paradigm**, combining object-oriented and functional
programming, with structured programming organizing the request/response flow.

## Object-oriented programming

Used through Django models, where each model is an entity with attributes and
behavior:

- `Area`
- `Employee`
- `Task`

See the [Data Model](data-model.md) for their fields and relationships.

## Functional programming

Used to process task data without mutating shared state — ideal for the
[reports](reports.md):

- Filter overdue tasks.
- Count completed tasks.
- Calculate productivity by area.
- Calculate deadline compliance.
- Sort tasks by priority.

These typically live in each module's `selectors.py` (read/query helpers).

## Structured programming

Used in the flow of views, forms, validations, and reports. A typical task
creation flow:

1. Receive task data.
2. Validate the data.
3. Save the task.
4. Show confirmation.
5. Update reports.

See the [creating a task](workflows.md#creating-a-task) activity diagram for a
visual version of this flow. Write-side orchestration lives in each module's
`services.py`.

## How paradigms map to the architecture

| Concern              | File              | Paradigm |
| -------------------- | ----------------- | -------- |
| Entities             | `models.py`       | OOP |
| Read queries / reports | `selectors.py`  | Functional |
| Write orchestration  | `services.py`     | Structured |
| Request handling     | `views.py`        | Structured |

See [Architecture → Module scaffolding](architecture.md#module-scaffolding).
