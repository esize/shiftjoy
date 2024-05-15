from celery import shared_task
from datetime import date, timedelta, datetime

from forecast.lib import get_days_in_week, get_variable_value, populate_weekly_defaults
from .models import ForecastVariable, VariableInstance
from teams.models import Location

@shared_task
def generate_variables(run_date: datetime):  # Runs 18 days prior to schedule start date
    if run_date is None:
        run_date = datetime.today()
    schedule_start_date = run_date + timedelta(days=18)
    print(f"Start Date: {schedule_start_date.date()}")
    schedule_start_weekday = schedule_start_date.strftime("%A")
    print(f"Start Day: {schedule_start_weekday}")
    
    locations_to_generate = Location.objects.all().filter(day_week_starts=schedule_start_weekday.upper())  # For example, schedules that begin on thursday will generate variables on a sunday
    if len(locations_to_generate) < 1:
        return ValueError("No variable exists")

    week_to_generate = get_days_in_week(schedule_start_date)
    
    populate_weekly_defaults(week=week_to_generate)

    for location in locations_to_generate:
        location_vars = location.variables.all()

        for v in location_vars:
            for d in week_to_generate:
                get_variable_value(d, v, update=True)
    
