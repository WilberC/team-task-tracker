# Phase 2 — Front desk (minimal)

[← Back to plan](README.md)

**Goal:** the minimum of Part 1 needed to create vehicles and a service order
that can **generate a job order**. Keep it simple — detail comes later.

**Depends on:** [Phase 1](phase-1-people.md).

**Entities:** [Client](../data-model.md#client), [Vehicle](../data-model.md#vehicle),
[Service Order](../data-model.md#service-order). See [Domain → Part 1](../domain.md#part-1--negotiation-front-desk).

## Clients module (`src/clients`)

- [ ] Scaffold module
- [ ] `Client` model (`full_name`, `phone`, `email`)
- [ ] Migration → confirm table `clients_client`
- [ ] Admin + list/create/edit views + templates
- [ ] Tests

## Vehicles module (`src/vehicles`)

- [ ] Scaffold module
- [ ] `Vehicle` model (`client` FK, `plate`, `make`, `model`, `year`)
- [ ] Migration → confirm table `vehicles_vehicle`
- [ ] Admin + list/create/edit views + templates
- [ ] Selector: vehicles by client
- [ ] Tests

## Sales / service orders module (`src/sales`)

- [ ] Scaffold module
- [ ] `ServiceOrder` model (`client`, `vehicle`, `advisor` FK nullable, `description`, `status`, `created_at`)
- [ ] Status enum (Open / Approved / Closed)
- [ ] Migration → confirm table `sales_serviceorder`
- [ ] Admin + list/create/edit views + templates
- [ ] `services.py`: `create_service_order(...)`
- [ ] Tests

## Definition of done

- [ ] An advisor can register a client + vehicle and create a service order
- [ ] A service order shows its client, vehicle, and status
- [ ] The data needed to generate a job order is captured (handed to [Phase 3](phase-3-job-orders.md))
- [ ] Tests passing
