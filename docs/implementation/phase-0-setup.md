# Phase 0 — Project setup & tooling

[← Back to plan](README.md)

**Goal:** a runnable, empty Django project with the `src/` layout, PostgreSQL,
and the frontend toolchain in place.

**Depends on:** nothing.

## Backend

- [x] Initialize `uv` project and add Django + `psycopg` (PostgreSQL driver)
- [x] Create the Django project config package `tracker/` (`settings.py`, `urls.py`, `asgi.py`, `wsgi.py`)
- [x] Create the `src/` package with `__init__.py`
- [x] Create `src/common/` app (shared mixins, validators, constants, helpers)
- [x] Add a `TimeStampedModel` mixin (`created_at` / `updated_at`) in `src/common`
- [x] Configure `settings.py`: installed apps, templates dir (`templates/`), static, database via env vars
- [x] Add `.env` handling (e.g. `django-environ`) and a `.env.example`
- [x] Connect to PostgreSQL and run `migrate` successfully
- [x] Create a superuser and confirm the Django admin loads

## Project conventions

- [x] Implement the `startmodule` management command (scaffolds the module structure from [Architecture](../architecture.md#module-scaffolding))
- [x] Document module creation in the README or a CONTRIBUTING note
- [x] Add code quality tooling (e.g. `ruff` for lint/format) and a pre-commit config

## Docker & containers

A `docker-compose` for local development (so devs get PostgreSQL with zero
setup) and a `Dockerfile` for the app (to make future deployment easy).

### Compose for local dev (database)

- [x] Add `docker-compose.yml` with a `db` service (PostgreSQL, pinned version)
- [x] Use a named volume for data persistence and expose port `5432`
- [x] Configure DB credentials/name via env vars matching `.env.example`
- [x] Document `docker compose up -d db` as the standard way to start the database
- [ ] (Optional) add an `adminer`/`pgadmin` service for inspecting the DB
- [x] Confirm `migrate` works against the Compose database

### Dockerfile for the app (future deployment)

- [x] Add a `Dockerfile` building the app with `uv` (multi-stage: build deps → slim runtime)
- [x] Build frontend assets (`pnpm` build) in the image and run `collectstatic`
- [x] Run via an ASGI server (for optional Channels) as a non-root user
- [x] Add a `.dockerignore` (`.git`, `node_modules`, `.venv`, build artifacts, `.env`)
- [x] (Optional) add an `app` service to `docker-compose.yml` for full local stack runs
- [x] Confirm the image builds and serves the base page

## Frontend toolchain

- [x] Initialize `pnpm` and the frontend build (e.g. Vite or esbuild)
- [x] Set up TypeScript config
- [x] Set up SCSS compilation with **Open Props** tokens
- [x] Add **htmx** to the base template
- [x] Wire compiled output to `static/css/main.css` and `static/js/`
- [x] Create `templates/base.html` with header/nav, content block, and asset includes
- [x] Add base layout styles (spacing, typography, color tokens) in `src/assets/scss`

## Repo hygiene

- [x] Add `.gitignore` (Python, node, env, build artifacts)
- [x] Add a `justfile`/`Makefile` or documented commands for run/test/build
- [x] First commit on a feature branch

## Definition of done

- [x] `docker compose up -d db` starts PostgreSQL and the app connects to it
- [x] `uv run python manage.py runserver` serves a styled base page
- [x] Admin login works against PostgreSQL
- [x] `pnpm` build produces CSS/JS picked up by `base.html`
- [x] The app `Dockerfile` builds successfully
