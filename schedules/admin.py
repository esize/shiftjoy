from django.contrib import admin

from .models import  SchedulePeriod, Schedule, Shift

admin.site.register(SchedulePeriod)
admin.site.register(Schedule)
admin.site.register(Shift)