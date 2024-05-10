from django.core.management.base import BaseCommand, CommandError
from dateutil import parser

from forecast.lib import get_days_in_week, populate_day_of_week_var, populate_start_of_day_var, populate_month_of_year_var, populate_day_of_year_var

class Command(BaseCommand):
    help = 'Generate the default variables for a given week'

    def handle(self, *args, **options):
        start_date_str = input("Which week should defaults be generated for?  ")
        start_date = parser.parse(start_date_str)
        week = get_days_in_week(start_date)

        try:
            week_vars = populate_day_of_week_var(week)
            self.stdout.write(self.style.SUCCESS(week_vars))
            start_day = populate_start_of_day_var(week)
            self.stdout.write(self.style.SUCCESS(start_day))
            month = populate_month_of_year_var(week)
            self.stdout.write(self.style.SUCCESS(month))
            date = populate_day_of_year_var(week)
            self.stdout.write(self.style.SUCCESS(date))
        except CommandError as e:
            self.stderr.write(self.style.ERROR_OUTPUT(e))