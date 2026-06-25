from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

MODULE_FILES = {
    "__init__.py": "",
    "admin.py": '"""Admin registrations for the {module} module."""\n',
    "forms.py": '"""Forms for the {module} module."""\n',
    "models.py": '"""Models for the {module} module."""\n',
    "selectors.py": '"""Read/query helpers for the {module} module."""\n',
    "services.py": '"""Write orchestration for the {module} module."""\n',
    "urls.py": (
        '"""URL routes for the {module} module."""\n\n'
        "from django.urls import path\n\n\n"
        'app_name = "{module}"\n\n'
        "urlpatterns = []\n"
    ),
    "views.py": '"""Views for the {module} module."""\n',
}

TEST_FILES = {
    "__init__.py": "",
    "test_models.py": '"""Model tests for the {module} module."""\n',
    "test_services.py": '"""Service tests for the {module} module."""\n',
    "test_views.py": '"""View tests for the {module} module."""\n',
}


class Command(BaseCommand):
    help = "Create a Django module under src/ using the project scaffold."

    def add_arguments(self, parser) -> None:
        parser.add_argument("name", help="Module name, e.g. tasks or employees")

    def handle(self, *args, **options) -> None:
        module = options["name"].strip()
        if not module.isidentifier() or not module.islower():
            raise CommandError("Module name must be a lowercase Python identifier.")

        module_dir = Path(settings.BASE_DIR) / "src" / module
        if module_dir.exists():
            raise CommandError(f"Module already exists: {module_dir}")

        class_name = "".join(part.capitalize() for part in module.split("_")) + "Config"
        module_dir.mkdir(parents=True)

        for relative_path, content in MODULE_FILES.items():
            (module_dir / relative_path).write_text(
                content.format(module=module),
                encoding="utf-8",
            )

        (module_dir / "apps.py").write_text(
            (
                "from django.apps import AppConfig\n\n\n"
                f"class {class_name}(AppConfig):\n"
                '    default_auto_field = "django.db.models.BigAutoField"\n'
                f'    name = "src.{module}"\n'
                f'    label = "{module}"\n'
            ),
            encoding="utf-8",
        )

        tests_dir = module_dir / "tests"
        tests_dir.mkdir()
        for relative_path, content in TEST_FILES.items():
            (tests_dir / relative_path).write_text(
                content.format(module=module),
                encoding="utf-8",
            )

        templates_dir = module_dir / "templates" / module
        templates_dir.mkdir(parents=True)

        scss_dir = module_dir / "assets" / "scss"
        scss_dir.mkdir(parents=True)
        (scss_dir / f"_{module}.scss").write_text("", encoding="utf-8")

        ts_dir = module_dir / "assets" / "ts"
        ts_dir.mkdir(parents=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created src/{module}. Add src.{module}.apps.{class_name} "
                "to INSTALLED_APPS."
            )
        )
