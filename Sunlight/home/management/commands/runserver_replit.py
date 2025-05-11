from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs the Django server for Replit environment'

    def handle(self, *args, **options):
        self.stdout.write('Starting Django server for Replit...')
        call_command(
            'runserver',
            '0.0.0.0:8000',
            use_reloader=False,
            use_threading=True
        )