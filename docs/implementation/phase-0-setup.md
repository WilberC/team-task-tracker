# Phase 0 — Project setup & tooling

[← Back to plan](README.md)

**Goal:** a runnable, empty Django project with the `src/` layout, PostgreSQL,
and the frontend toolchain in place.

**Depends on:** nothing.

## Backend

- [ ] Initialize `uv` project and add Django + `psycopg` (PostgreSQL driver)
- [ ] Create the Django project config package `tracker/` (`settings.py`, `urls.py`, `asgi.py`, `wsgi.py`)
- [ ] Create the `src/` package with `__init__.py`
- [ ] Create `src/common/` app (shared mixins, validators, constants, helpers)
- [ ] Add a `TimeStampedModel` mixin (`created_at` / `updated_at`) in `src/common`
- [ ] Configure `settings.py`: installed apps, templates dir (`templates/`), static, database via env vars
- [ ] Add `.env` handling (e.g. `django-environ`) and a `.env.example`
- [ ] Connect to PostgreSQL and run `migrate` successfully
- [ ] Create a superuser and confirm the Django admin loads

## Project conventions

- [ ] Implement the `startmodule` management command (scaffolds the module structure from [Architecture](../architecture.md#module-scaffolding))
- [ ] Document module creation in the README or a CONTRIBUTING note
- [ ] Add code quality tooling (e.g. `ruff` for lint/format) and a pre-commit config

## Docker & containers

A `docker-compose` for local development (so devs get PostgreSQL with zero
setup) and a `Dockerfile` for the app (to make future deployment easy).

### Compose for local dev (database)

- [ ] Add `docker-compose.yml` with a `db` service (PostgreSQL, pinned version)
- [ ] Use a named volume for data persistence and expose port `5432`
- [ ] Configure DB credentials/name via env vars matching `.env.example`
- [ ] Document `docker compose up -d db` as the standard way to start the database
- [ ] (Optional) add an `adminer`/`pgadmin` service for inspecting the DB
- [ ] Confirm `migrate` works against the Compose database

### Dockerfile for the app (future deployment)

- [ ] Add a `Dockerfile` building the app with `uv` (multi-stage: build deps → slim runtime)
- [ ] Build frontend assets (`pnpm` build) in the image and run `collectstatic`
- [ ] Run via an ASGI server (for optional Channels) as a non-root user
- [ ] Add a `.dockerignore` (`.git`, `node_modules`, `.venv`, build artifacts, `.env`)
- [ ] (Optional) add an `app` service to `docker-compose.yml` for full local stack runs
- [ ] Confirm the image builds and serves the base page

## Frontend toolchain

- [ ] Initialize `pnpm` and the frontend build (e.g. Vite or esbuild)
- [ ] Set up TypeScript config
- [ ] Set up SCSS compilation with **Open Props** tokens
- [ ] Add **htmx** to the base template
- [ ] Wire compiled output to `static/css/main.css` and `static/js/`
- [ ] Create `templates/base.html` with header/nav, content block, and asset includes
- [ ] Add base layout styles (spacing, typography, color tokens) in `src/assets/scss`

## Repo hygiene

- [ ] Add `.gitignore` (Python, node, env, build artifacts)
- [ ] Add a `justfile`/`Makefile` or documented commands for run/test/build
- [ ] First commit on a feature branch

## Definition of done

- [ ] `docker compose up -d db` starts PostgreSQL and the app connects to it
- [ ] `uv run python manage.py runserver` serves a styled base page
- [ ] Admin login works against PostgreSQL
- [ ] `pnpm` build produces CSS/JS picked up by `base.html`
- [ ] The app `Dockerfile` builds successfully
