from django.contrib import admin
from django.forms import RadioSelect, Select
from .models import *
from django.db import models
from .forms import PositionForm
from django.templatetags.static import static
from django.utils.html import format_html
from semantic_admin import SemanticModelAdmin, SemanticStackedInline, SemanticTabularInline

# Register your models here.

@admin.register(Condition)
class ConditionAdmin(SemanticModelAdmin):
    model = Condition

@admin.register(VariableBehavior)
class VariableBehaviorAdmin(SemanticModelAdmin):
    model = VariableBehavior

@admin.register(CalculatedValue)
class CalculatedValueAdmin(SemanticModelAdmin):
    model = CalculatedValue

@admin.register(PositionBehavior)
class PositionBehaviorAdmin(SemanticModelAdmin):
    model = PositionBehavior
    extra = 1


@admin.register(ForecastVariable)
class ForecastVariableAdmin(SemanticModelAdmin):
    model = ForecastVariable
    list_display = ['__str__', 'type', 'frequency', 'format', 'location']

    class Media:
        js = [format_html(
            '<script type="module" src="{}"></script>', 
            static('js/forecast/variable.js')
        )]

@admin.register(Position)
class PositionAdmin(SemanticModelAdmin):
    model = Position
    fieldsets = (
        ("Basic Information", {
            'fields': ('name','active',('type', 'frequency', 'format',), 'team', 'color',)
        }),
        ("Constraints", {
            'fields': ('minimum_age', 'gender_specific', 'required_gender',),
            'classes': ('predefined',)
        }),
        (None, {
            'fields': ('skills','unbudgeted')
        })
    )

    # inlines = (PositionBehaviorAdmin,)

    formfield_overrides = {
        models.Choices: {"widget": RadioSelect}
    }
    class Media:
        js = [format_html(
            '<script type="module" src="{}"></script>', 
            static('js/forecast/position.js')
        )]

@admin.register(VariableInstance)
class VariableInstanceAdmin(SemanticModelAdmin):
    model = VariableInstance

@admin.register(Skill)
class SkillAdmin(SemanticModelAdmin):
    model = Skill