from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from semantic_admin import SemanticModelAdmin, SemanticTabularInline

from .models import Employee, EmployeeSkill, Availability, AvailabilityPeriod
from .forms import EmployeeCreationForm


class EmployeeSkillAdmin(SemanticTabularInline):
    model = EmployeeSkill
    extra = 1

@admin.register(Employee)
class EmployeeAdmin(SemanticModelAdmin, UserAdmin):
    fieldsets = None
    # fields = ["username", "first_name", "last_name", "home_team", "status", "employment_type", "managed_teams"]
    model = Employee
    list_display = ["employee_id", "name", "home_team", "employment_type"]
    autocomplete_fields = ['home_team', 'managed_teams']
    readonly_fields = ['employee_id']
    add_form = EmployeeCreationForm
    fieldsets = (
        
        (
            "Employee Information",
            {
                "classes": ("wide",),
                "fields": ("employee_id", ("first_name", "last_name",),( "home_team", "employment_type"), "managed_teams")
            }
        ),(
            ("Permissions"),
            {
                "fields": (
                    "groups",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            "Login",
            {
                "classes": ("wide",),
                "fields": ("username",),
            },
        ),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
        (
            "Employee Information",
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "home_team", "employment_type", "managed_teams")
            }
        ),
    )

    inlines = [EmployeeSkillAdmin,]

    @admin.display(description="Employee ID")
    def employee_id(self, obj):
        return obj.username
    
    @admin.display(description="Name")
    def name(self, obj):
        return obj.get_full_name()


admin.site.register(Availability)
admin.site.register(AvailabilityPeriod)
