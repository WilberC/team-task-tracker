from django.db import migrations

EXAMPLE_AREAS = [
    ("Mechanical", "General mechanical diagnosis, repair, and maintenance."),
    ("Bodywork", "Panel repair and bodywork preparation."),
    ("Paint", "Paint preparation, color matching, and finishing."),
    ("Electrical", "Electrical diagnosis, wiring, and electronic systems."),
]


def seed_example_areas(apps, schema_editor):
    area_model = apps.get_model("areas", "Area")
    for name, description in EXAMPLE_AREAS:
        area_model.objects.get_or_create(
            name=name,
            defaults={
                "description": description,
                "active": True,
            },
        )


def remove_example_areas(apps, schema_editor):
    area_model = apps.get_model("areas", "Area")
    area_model.objects.filter(name__in=[name for name, _ in EXAMPLE_AREAS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("areas", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_example_areas, remove_example_areas),
    ]
