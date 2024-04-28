from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ForecastVariable)
admin.site.register(CalculatedValue)
admin.site.register(Condition)
admin.site.register(VariableBehavior)
admin.site.register(VariableInstance)
admin.site.register(Skill)
admin.site.register(Position)
admin.site.register(PositionBehavior)