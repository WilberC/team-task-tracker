"""Django settings for Team Task Tracker."""

from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1", "0.0.0.0"]),
    DJANGO_CSRF_TRUSTED_ORIGINS=(list, []),
)
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-only-change-me")
if not DEBUG and SECRET_KEY == "dev-only-change-me":
    raise ImproperlyConfigured("Set DJANGO_SECRET_KEY before running in production.")
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0"],
)
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=not DEBUG)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
if env.bool("DJANGO_USE_X_FORWARDED_PROTO", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "src.access.apps.AccessConfig",
    "src.common.apps.CommonConfig",
    "src.areas.apps.AreasConfig",
    "src.employees.apps.EmployeesConfig",
    "src.teams.apps.TeamsConfig",
    "src.clients.apps.ClientsConfig",
    "src.vehicles.apps.VehiclesConfig",
    "src.sales.apps.SalesConfig",
    "src.workshop.apps.WorkshopConfig",
    "src.tasks.apps.TasksConfig",
    "src.dashboard.apps.DashboardConfig",
    "src.reports.apps.ReportsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "src.access.middleware.AdminRoleRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "src.access.context_processors.access",
            ],
        },
    },
]

WSGI_APPLICATION = "tracker.wsgi.application"
ASGI_APPLICATION = "tracker.asgi.application"

db_name = env("POSTGRES_DB", default="tracker")
db_user = env("POSTGRES_USER", default="tracker")
db_password = env("POSTGRES_PASSWORD", default="tracker")
db_host = env("POSTGRES_HOST", default="localhost")
db_port = env("POSTGRES_PORT", default="5432")
default_database_url = (
    f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
DATABASES = {
    "default": env.db("DATABASE_URL", default=default_database_url),
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
staticfiles_storage = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
    if DEBUG
    else "whitenoise.storage.CompressedManifestStaticFilesStorage"
)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": staticfiles_storage,
    },
}
WHITENOISE_MAX_AGE = env.int(
    "WHITENOISE_MAX_AGE",
    default=60 if DEBUG else 31536000,
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "post_login"
LOGOUT_REDIRECT_URL = "home"

LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "src": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

SEED_USER_PASSWORD = env("SEED_USER_PASSWORD", default="")
TEST_ACCOUNT_EMAILS = env.list("TEST_ACCOUNT_EMAILS", default=[])
TEST_ACCOUNTS_UNLOCK_PASSWORD = env("TEST_ACCOUNTS_UNLOCK_PASSWORD", default="")
