# Phase 2 — Front desk (minimal)

[← Back to plan](README.md)

**Goal:** the minimum of Part 1 needed to create vehicles and a service order
that can **generate a job order**. Keep it simple — detail comes later.

**Depends on:** [Phase 1](phase-1-people.md).

**Entities:** [Client](../data-model.md#client), [Vehicle](../data-model.md#vehicle),
[Service Order](../data-model.md#service-order). See [Domain → Part 1](../domain.md#part-1--negotiation-front-desk).

## Clients module (`src/clients`)

- [x] Scaffold module
- [x] `Client` model (`full_name`, `phone`, `email`)
- [x] Migration → confirm table `clients_client`
- [x] Admin + list/create/edit views + templates
- [x] Tests

## Vehicles module (`src/vehicles`)

- [x] Scaffold module
- [x] `Vehicle` model (`client` FK, `plate`, `make`, `model`, `year`)
- [x] Migration → confirm table `vehicles_vehicle`
- [x] Admin + list/create/edit views + templates
- [x] Selector: vehicles by client
- [x] Tests

## Sales / service orders module (`src/sales`)

- [x] Scaffold module
- [x] `ServiceOrder` model (`client`, `vehicle`, `advisor` FK nullable, `description`, `status`, `created_at`)
- [x] Status enum (Open / Approved / Closed)
- [x] Migration → confirm table `sales_serviceorder`
- [x] Admin + list/create/edit views + templates
- [x] `services.py`: `create_service_order(...)`
- [x] Tests

## Definition of done

- [x] An advisor can register a client + vehicle and create a service order
- [x] A service order shows its client, vehicle, and status
- [x] The data needed to generate a job order is captured (handed to [Phase 3](phase-3-job-orders.md))
- [x] Tests passing
