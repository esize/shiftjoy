from datetime import datetime
from django.core.management.base import BaseCommand, CommandError, CommandParser
from forecast.tasks import generate_variables

class Command(BaseCommand):
    help = 'Generate the variables for a week (run daily)'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("dayofmonth", nargs='?', type=int, default=datetime.today().day)

    def handle(self, *args, **options):
        default_date = datetime.today()
        day = options['dayofmonth']
        run_date = default_date.replace(day=day)
        self.stdout.write(self.style.WARNING(f"Run Date: ") + str(run_date.date()))
        gen = generate_variables(run_date=run_date)
        if gen is not None:
            self.stderr.write(self.style.ERROR("No variables to generate today!"))
        else:
            self.stdout.write(
                self.style.SUCCESS('Done!')
            )