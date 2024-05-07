from datetime import timedelta, date, datetime, time
from forecast.models import ForecastVariable, VariableInstance, CalculatedValue


def get_days_in_week(start_date: date) -> list[date]:
    dates = []

    for d in range(7):
        dates.append(start_date + timedelta(days=d))
    return dates
    
def infer_type(var):
    if 'True' in str(var):
        return True
    elif 'False' in str(var):
        return False
    elif str(var).isalpha():
        return var
    try:
        return datetime.strptime(str(var), "%H:%M:%S").time()
    except:
        try:
            return int(var)
        except:
            return float(var)
    
def calc(value_calculated: CalculatedValue, date: date):

    v1 = infer_type(VariableInstance.objects.get(variable=value_calculated.variable, date=date).value)
    op = value_calculated.operator
    v2 = None

    if value_calculated.value is not None:
        v2 = infer_type(value_calculated.value)
    else:
        v2 = infer_type(VariableInstance.objects.get(variable=value_calculated.value_variable, date=date).value)
    
    

    if type(v1) == type(time()) and isinstance(v2, (int, float)):
        print(v1)
        dt1 = datetime(1970,1,1,v1.hour,v1.minute)
        if op == 'ADD':
            return (dt1 + timedelta(hours=v2)).time()
        return (dt1 - timedelta(hours=v2)).time()
    elif type(v1) == type(time()) and type(v2) == type(time()):
        print(v1)
        dt1 = datetime(1970,1,1,v1.hour,v1.minute)
        if op == 'ADD':
            return (dt1 + timedelta(hours=v2.hour,minutes=v2.minute)).time()
        return (dt1 - timedelta(hours=v2.hour,minutes=v2.minute)).time()

    if op == "ADD":
        return v1 + v2

    return v1 - v2
    
        

def get_variable_value(date: date, variable: ForecastVariable) -> str:
    if variable.type == 'VALUE':
        return str(variable.default_value)
    
    if variable.type == 'CALCULATED':
        for behavior in variable.behaviors.all():
                for condition in behavior.conditions.all():
                    var1_model = VariableInstance.objects.get(variable=condition.variable, date=date)
                    # print(var1_model.value)
                    var1 = infer_type(var1_model.value)

                    if condition.comparison_value is not None:
                        var2 = infer_type(condition.comparison_value)
                    else:
                        var2_model = VariableInstance.objects.get(variable=condition.comparison_variable, date=date)
                        try:
                            var2 = VariableInstance.objects.get(variable=var2_model, date=date)
                        except:
                            ValueError("Comparison Variable not yet defined.")

                    # print(f"{var1} {condition.comparison_operator} {var2}")

                    if condition.comparison_operator == "LT":
                        if var1 < var2:
                            continue
                        else:
                            print("STOP")
                            break
                    elif condition.comparison_operator == "LE":
                        if var1 <= var2:
                            continue
                        else:
                            break
                    elif condition.comparison_operator == "GT":
                        if var1 > var2:
                            continue
                        else:
                            break
                    elif condition.comparison_operator == "GE":
                        if var1 >= var2:
                            pass
                        else:
                            break
                    elif condition.comparison_operator == "EQ":
                        if var1 == var2:
                            pass
                        else:
                            break
                    elif condition.comparison_operator == "NE":
                        if var1 != var2:
                            pass
                        else:
                            break
                else:
                    return calc(behavior.value_calculated, date)
        if variable.default_value is not None:
            return variable.default_value
        return calc(variable.calculated_default_value, date)