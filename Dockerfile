FROM node:22-bookworm-slim AS frontend
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY src ./src
COPY tsconfig.json vite.config.ts ./
RUN pnpm build

FROM python:3.13-slim AS python-deps
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
COPY --from=ghcr.io/astral-sh/uv:0.11.24 /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

FROM python:3.13-slim AS runtime
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=python-deps /app/.venv /app/.venv
COPY --from=frontend /app/static /app/static
COPY manage.py pyproject.toml ./
COPY tracker ./tracker
COPY src ./src
COPY templates ./templates

RUN DJANGO_SECRET_KEY=build-only-collectstatic python manage.py collectstatic --noinput

USER app
EXPOSE 8000
CMD ["uvicorn", "tracker.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
