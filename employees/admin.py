from django.contrib import admin

from .models import Employee, EmployeeSkill, Availability, AvailabilityPeriod

admin.site.register(Employee)
admin.site.register(EmployeeSkill)
admin.site.register(Availability)
admin.site.register(AvailabilityPeriod)
