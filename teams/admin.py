from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from semantic_admin import SemanticModelAdmin, SemanticStackedInline, SemanticTabularInline

from .models import Organization, Location, Team

@admin.register(Team)
class TeamAdmin(SemanticModelAdmin):
    fieldsets = None
    model = Team
    search_fields = ['name']

@admin.register(Organization)
class OrganizationAdmin(SemanticModelAdmin):
    model = Organization

@admin.register(Location)
class LocationAdmin(SemanticModelAdmin):
    model = Location