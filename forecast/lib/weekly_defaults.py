from datetime import date, time
from forecast.models import ForecastVariable, VariableInstance


def populate_day_of_week_var(week: list[date]) -> list[VariableInstance]:
    v = ForecastVariable.objects.get(name="Day of Week")
    return_list = []
    for day in week:
        try:
            return_list.append(VariableInstance.objects.update_or_create(variable=v, date=day, defaults={"value": day.strftime('%A')})[0])
        except:
            pass
    return return_list

def populate_start_of_day_var(week: list[date]) -> list[VariableInstance]:
    v = ForecastVariable.objects.get(name="Start of Day")
    return_list = []
    for day in week:
        try:
            start_day_time = time(0,0)
            return_list.append(VariableInstance.objects.update_or_create(variable=v, date=day, defaults={"value": start_day_time})[0])
        except:
            pass
    return return_list


def populate_month_of_year_var(week: list[date]) -> list[VariableInstance]:
    v = ForecastVariable.objects.get(name="Month of Year")
    return_list = []
    for day in week:
        try:
            month = day.strftime('%B')
            return_list.append(VariableInstance.objects.update_or_create(variable=v, date=day, defaults={"value": month})[0])
        except ValueError:
            raise ValueError
    return return_list


def populate_day_of_year_var(week: list[date]) -> list[VariableInstance]:
    v = ForecastVariable.objects.get(name="Day of Year")
    return_list = []
    for day in week:
        try:
            year = day.strftime('%j')
            return_list.append(VariableInstance.objects.update_or_create(variable=v, date=day, defaults={"value": year})[0])
        except ValueError:
            raise ValueError
    return return_list