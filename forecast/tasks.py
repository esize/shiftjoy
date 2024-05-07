from celery import shared_task
from datetime import date, timedelta, datetime

from forecast.lib import get_days_in_week

from .models import ForecastVariable, VariableInstance

@shared_task
def generate_variables(start_date):
    dates = get_days_in_week(start_date)

    for date in dates:
        for variable in ForecastVariable.objects.get(type='VALUE'):
            VariableInstance.objects.create(
                variable=variable,
                value=variable.default_value,
                date=date,
            )
        
        for variable in ForecastVariable.objects.get(type='CALCULATED'):
            var_val = ''
            for behavior in variable.behaviors:
                truthy = True
                for condition in behavior:
                    init = condition.variable.value
                    if condition.comparison_value is not None:
                        comp = condition.comparison_value
                    else:
                        comp = condition.comparison_variable.value

                    if condition.comparison_operator == "LT":
                        if init < comp:
                            pass
                        else:
                            truthy=False
                            break
                    elif condition.comparison_operator == "LE":
                        if init <= comp:
                            pass
                        else:
                            truthy=False
                            break
                    elif condition.comparison_operator == "GT":
                        if init > comp:
                            pass
                        else:
                            truthy=False
                            break
                    elif condition.comparison_operator == "GE":
                        if init >= comp:
                            pass
                        else:
                            truthy=False
                            break
                    elif condition.comparison_operator == "EQ":
                        if init == comp:
                            pass
                        else:
                            truthy=False
                            break
                    elif condition.comparison_operator == "NE":
                        if init != comp:
                            pass
                        else:
                            truthy=False
                            break

                if truthy:
                    var_val = behavior.value
    
