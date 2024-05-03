from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Organization, Location, Team

admin.site.register(Organization)
admin.site.register(Location)
admin.site.register(Team, MPTTModelAdmin)