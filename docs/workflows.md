# Workflows

[← Back to README](../README.md)

This document describes how work moves through the [workshop](domain.md) over
time. For the static definitions of each entity and status, see
[Features](features.md) and the [Data Model](data-model.md).

## Workshop flow (service order → job order → tasks)

The end-to-end path of a vehicle through the shop:

```plantuml
@startuml
start
partition "Front desk (Part 1)" {
  :Advisor negotiates work with client;
  :Create Service Order;
  if (Approved?) then (yes)
    :Generate **Job Order** (job order id);
  else (no)
    stop
  endif
}
partition "Workshop (Part 2)" {
  :Intern (check in) the vehicle;
  :Add **Diagnostic** as a top-level task,\nassigned to a mechanic;
  :Define the jobs to do (top-level tasks);
  :Break each job into subtasks;
  :Assign each task (mechanic or team);
  repeat
    :Mechanics update task status;
  repeat while (All tasks done?) is (no)
  ->yes;
  :Close job order;
  :Deliver vehicle;
}
stop
@enduml
```

The client can follow the vehicle's status throughout — see
[client status view](#client-status-view).

## Task lifecycle

A task is created as **Pending** and moves through its statuses as work
progresses. If the due date passes before completion, the system marks it as
**Overdue**. A task can be **Cancelled** at any point before completion.

```plantuml
@startuml
hide empty description

[*] --> Pending : task created

Pending --> InProgress : work starts
InProgress --> Completed : work finished
Pending --> Overdue : due date passed
InProgress --> Overdue : due date passed
Overdue --> Completed : finished (late)

Pending --> Cancelled : no longer needed
InProgress --> Cancelled : no longer needed

Completed --> [*]
Cancelled --> [*]

state Completed : completion_date recorded
state Overdue : due_date < today
@enduml
```

## Creating a task

A user creates a task by entering its information. The task starts in the
**Pending** status.

```plantuml
@startuml
start
:Open the job order (top-level task)\nor pick a parent task (subtask);
:Add title and description;
:Assign a mechanic or a team;
:Select area and priority;
:Set due date;
:Save task;
if (Data valid?) then (yes)
  :Create task with status = Pending;
  :Show confirmation;
  :Update dashboard counters;
else (no)
  :Show validation errors;
  stop
endif
stop
@enduml
```

## Assigning and completing a task

- A task is assigned to a **mechanic or a team**. They become responsible for
  completing it before the due date.
- The status is updated as work progresses
  (`Pending → In progress → Completed`).
- When finished, the responsible employee sets the status to **Completed**, and
  the system stores the completion date to determine whether it was on time or
  late.
- If the due date passes without completion, the system can mark the task as
  **Overdue**.

## Subtask progress roll-up

When a task is [split into subtasks](data-model.md#subtasks), the parent's
progress is derived from its children so the person in charge always sees an
honest picture without manual bookkeeping.

- The parent shows a count like **"2 of 3 done"** and a progress bar.
- A parent is considered **Completed** only when **all** its subtasks are
  Completed or Cancelled.
- If any subtask is **Overdue**, the parent is flagged as at risk.

```plantuml
@startuml
start
:Subtask status changes;
:Recount parent's subtasks;
if (All subtasks Completed or Cancelled?) then (yes)
  :Mark parent Completed;
  :Record completion_date;
else (no)
  if (Any subtask Overdue?) then (yes)
    :Flag parent as at risk;
  else (no)
    :Update parent progress (e.g. 2 of 3);
  endif
endif
stop
@enduml
```

## End-to-end user flow

The typical flow across roles, from intake to delivery:

```plantuml
@startuml
actor Advisor
actor Mechanic
actor Client
participant "Task Tracker" as Sys
database "PostgreSQL" as DB

Advisor -> Sys : Register client + vehicle, create service order
Sys -> DB : Save client, vehicle, service order
Advisor -> Sys : Approve service order
Sys -> DB : Generate job order (job order id)

Advisor -> Sys : Intern vehicle, assign diagnostic to a mechanic
Sys -> DB : Save top-level task (status = Pending)

Mechanic -> Sys : Add jobs + subtasks, assign mechanic/team
Sys -> DB : Save tasks

Mechanic -> Sys : Update task status (In progress / Completed)
Sys -> DB : Update task
Sys -> Sys : Roll up subtask progress to parent and job order

Client -> Sys : Open client status view
Sys -> DB : Read job order progress
Sys --> Client : Vehicle status (read-only)
@enduml
```

## Related documents

- [Features](features.md) — definitions of statuses and priorities.
- [Reports](reports.md) — the outputs produced from this data.
- [Paradigms](paradigms.md) — how these flows map to the code's structure.
