from django.core.management.base import BaseCommand, CommandError
from forecast.lib import s

class Command(BaseCommand):
    help = 'Run the scratch file'

    def handle(self, *args, **options):
        s()
        self.stdout.write(
            self.style.SUCCESS('It worked! Scratch yourself on the back...')
        )