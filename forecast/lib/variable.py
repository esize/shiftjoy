from datetime import timedelta, date, datetime, time
from forecast.models import ForecastVariable, VariableInstance, CalculatedValue

def get_days_in_week(start_date: date) -> list[date]:
    """Return a list date objects for the week beginning on start_date"""
    dates = []

    for d in range(7):
        dates.append(start_date + timedelta(days=d))
    return dates
    
def infer_type(var):
    """Convert the variable value to its native python type"""

    if var.value is not None:  # If a variable instance is passed in, use the variable value
        var = var.value

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
    
def calc(formula: CalculatedValue, date: date):
    """Calculate a variable value. Will recursively call get_variable_value if the value has not yet been created."""

    var1 = infer_type(get_variable_value(date, formula.variable))
    operator = formula.operator
    var2 = None

    if formula.value is not None:
        var2 = infer_type(formula.value)
    else:
        var2 = infer_type(get_variable_value(date, formula.value_variable))
    
    

    d = date
    if type(var1) == type(time()) and isinstance(var2, (int, float)):
        print(var1)
        dt1 = datetime(d.year, d.month, d.day, var1.hour,var1.minute)
        if operator == 'ADD':
            return (dt1 + timedelta(hours=var2)).time()
        return (dt1 - timedelta(hours=var2)).time()
    elif type(var1) == type(time()) and type(var2) == type(time()):
        print(var1)
        dt1 = datetime(d.year, d.month, d.day, var1.hour,var1.minute)
        if operator == 'ADD':
            return (dt1 + timedelta(hours=var2.hour,minutes=var2.minute)).time()
        return (dt1 - timedelta(hours=var2.hour,minutes=var2.minute)).time()

    if operator == "ADD":
        return var1 + var2

    return var1 - var2
    
        

def get_variable_value(date: date, variable: ForecastVariable, update: bool=False) -> VariableInstance:
    """Get the value of a variable on a particular date, creating it in the database if it does not already exist.
    
    Args:
        `date`:
            A date to search for a particular variable on
        `variable`:
            The `ForecastVariable` object to search for
        `update`:
            Optional boolean specifying if an existing instance of `variable` on `date` should be overridden
    """
    if not update:
        #  Check if the variable value already exists before doing a bunch of hard work
        try:
            return VariableInstance.objects.get(date=date, variable=variable)
        except:
            print(f"No instance of {variable} defined on {date.strftime('%m/%d/%Y')}")

    #  Return default for value variables
    if variable.type == 'VALUE':
        default = variable.default_value
        return VariableInstance.objects.update_or_create(variable=variable, date=date, defaults={"value": default})


    if variable.type == 'CALCULATED':
        #  Loop through behaviors. Use behavior value or value calculation if all conditions are met.
        if len(variable.behaviors) > 0:  # Only loop through behaviors if they exist
            for behavior in variable.behaviors.all():
                    for condition in behavior.conditions.all():
                        var1_model = VariableInstance.objects.get(variable=condition.variable, date=date)
                        var1 = infer_type(var1_model.value)

                        if condition.comparison_value is not None:  # If the second value is just a value
                            var2 = infer_type(condition.comparison_value)
                        else:  # If the second value is another variable
                            var2_model = VariableInstance.objects.get(variable=condition.comparison_variable, date=date)
                            try:
                                var2 = VariableInstance.objects.get(variable=var2_model, date=date)
                            except:
                                ValueError("Comparison Variable not yet defined.")

                        #  Evaluate expression based on text input
                        if condition.comparison_operator == "LT":
                            if var1 < var2:
                                continue
                            else:
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

                    else: # If all conditions are met (loop is not broken), create and return the behavior value
                        if behavior.value is not None:  # If the behavior value is defined
                            return VariableInstance.objects.update_or_create(variable=variable, date=date, defaults={"value": behavior.value})

                        #  If the behavior value calculation is defined
                        val = calc(behavior.value_calculated, date)
                        return VariableInstance.objects.update_or_create(variable=variable, date=date, defaults={"value": val})
                    
        # If no behavior matches, return default
        if variable.default_value is not None:  # Return if default value is specified
            return VariableInstance.objects.update_or_create(variable=variable, date=date, defaults={"value": variable.default_value})
        
        # Calculate the default value if it is specified as calculated
        value = calc(variable.calculated_default_value, date)
        return VariableInstance.objects.update_or_create(variable=variable, date=date, defaults={"value": value})