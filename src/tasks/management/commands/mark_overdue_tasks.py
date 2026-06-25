from django.core.management.base import BaseCommand

from src.tasks.services import mark_overdue_tasks


class Command(BaseCommand):
    help = "Mark pending or in-progress tasks as overdue when their due date passed."

    def handle(self, *args, **options):
        count = mark_overdue_tasks()
        self.stdout.write(self.style.SUCCESS(f"Marked {count} task(s) as overdue."))
