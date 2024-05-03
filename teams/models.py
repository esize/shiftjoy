from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from forecast.models import Skill


class Organization(models.Model):
    name = models.CharField(max_length=256)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    enable_shiftplanning_export = models.BooleanField(default=False)
    enable_timeclock_default = models.BooleanField(default=False)
    enable_time_off_requests_default = models.BooleanField(default=False)
    shifts_assigned_days_before_start = models.IntegerField(default=4, blank=False, null=False)

    def __str__(self):
        return self.name


class Location(models.Model):
    DAY_CHOICES = {
        "MONDAY": "Monday",
        "TUESDAY": "Tuesday",
        "WEDNESDAY": "Wednesday",
        "THURSDAY": "Thursday",
        "FRIDAY": "Friday",
        "SATURDAY": "Saturday",
        "SUNDAY": "Sunday",
    }
    name = models.CharField(max_length=256)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    timezone = models.CharField(max_length=64, default='UTC', blank=False, null=False)
    day_week_starts = models.CharField(max_length=256, choices=DAY_CHOICES, default="Monday")

    def __str__(self):
        return self.name

class Team(MPTTModel):
    name = models.CharField(max_length=256)
    abbreviation = models.CharField(max_length=5, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_of_day = models.TimeField(default='00:00:00')
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name
