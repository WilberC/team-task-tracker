# Deployment Runbook

[← Back to docs](../README.md)

This runbook covers the Dockploy production path for Team Task Tracker.

## Required services

- PostgreSQL 17 or compatible managed PostgreSQL.
- A Dockploy application built from this repository's `Dockerfile`.
- A reverse proxy or platform router that terminates HTTPS.
- Persistent database backups outside the app container.

## Required environment

Set these values in the deployment platform:

```bash
DJANGO_SECRET_KEY=<strong-random-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tracker.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://tracker.example.com
DATABASE_URL=postgres://<user>:<password>@<host>:5432/<database>
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_USE_X_FORWARDED_PROTO=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True
WHITENOISE_MAX_AGE=31536000
```

Only set `DJANGO_SECURE_HSTS_PRELOAD=True` after the domain is ready for browser
HSTS preload requirements.

## Build

The Docker image builds frontend assets, installs Python dependencies, and runs
`collectstatic`. Dockploy can build it directly from the repository:

```bash
docker build -t team-task-tracker:<version> .
```

For non-Docker platforms, run the same steps explicitly:

```bash
uv sync --frozen --no-dev
pnpm install --frozen-lockfile
pnpm build
uv run python manage.py collectstatic --noinput
```

## Release

1. Confirm the predeploy checks pass for the commit being deployed.
2. Provision or verify the PostgreSQL database and `DATABASE_URL`.
3. Configure the Dockploy app with the production environment variables.
4. Deploy the new image from Dockploy.
5. Run migrations in the deployed app container:

   ```bash
   python manage.py migrate --noinput
   ```

6. Run a smoke check in the deployed app container:

   ```bash
   python manage.py check --deploy
   ```

7. Open the site over HTTPS and verify:
   - The login page loads.
   - An internal user can reach the dashboard or task list.
   - Static CSS and JavaScript are served.
   - A known client status token loads only the public status page.

## Rollback

1. Stop routing traffic to the failed release.
2. Redeploy the previous known-good Dockploy deployment.
3. If the failed release ran irreversible migrations, restore the latest database
   backup into a new database and point `DATABASE_URL` to it.
4. Run the smoke check again before restoring normal traffic.
5. Record the failed version, error, database state, and rollback time in the
   deployment log.
