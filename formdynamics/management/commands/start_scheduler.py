from django.core.management.base import BaseCommand
from scheduler import run_scheduler  # Make sure the import path is correct

class Command(BaseCommand):
    help = 'Starts the scheduler for Zoho API calls'

    def handle(self, *args, **kwargs):
        run_scheduler()