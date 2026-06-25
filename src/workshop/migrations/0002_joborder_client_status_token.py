"""Add public client status tokens to job orders."""

import uuid

from django.db import migrations, models


def populate_client_status_tokens(apps, schema_editor):
    job_order_model = apps.get_model("workshop", "JobOrder")
    for job_order in job_order_model.objects.filter(client_status_token__isnull=True):
        job_order.client_status_token = uuid.uuid4()
        job_order.save(update_fields=["client_status_token"])


class Migration(migrations.Migration):
    dependencies = [
        ("workshop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="joborder",
            name="client_status_token",
            field=models.UUIDField(
                editable=False,
                null=True,
                verbose_name="token para vista de cliente",
            ),
        ),
        migrations.RunPython(
            populate_client_status_tokens,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="joborder",
            name="client_status_token",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                verbose_name="token para vista de cliente",
            ),
        ),
    ]
