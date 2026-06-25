set dotenv-load := true

db:
    docker compose up -d db

install:
    uv sync
    pnpm install

migrate:
    uv run python manage.py migrate

superuser:
    uv run python manage.py createsuperuser --noinput

run:
    uv run python manage.py runserver

frontend:
    pnpm build

lint:
    uv run ruff check .
    uv run ruff format --check .

format:
    uv run ruff check --fix .
    uv run ruff format .

docker-build:
    docker build -t team-task-tracker .
