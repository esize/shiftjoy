from datetime import date
from forecast.models import ForecastVariable, VariableInstance
from forecast.lib import get_days_in_week, get_variable_value


def scratch():
    w = get_days_in_week(date(2024,5,30))
    v = ForecastVariable.objects.get(name="OPS - Kumba Closing - CALC")

    for d in w:
        val = get_variable_value(d,v)
        print(d.strftime("%m/%d/%Y"), val)
        print("")
        

