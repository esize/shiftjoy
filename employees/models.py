from django.contrib.auth.models import User
from django.db import models

from forecast.models import Skill
from teams.models import Team


class Employee(models.Model):
    STATUS_CHOICES = {
        'ONBOARDING': 'Onboarding',
        'ACTIVE': 'Active',
        'LEAVE': 'On Leave',
        'SUSPENDED': 'Suspended',
        'TERMINATED': 'Terminated',
    }
    TYPE_CHOICES = {
        'OFFICER': 'Officer',
        'FULL_TIME_SALARIED': 'Full Time (Salaried)',
        'FULL_TIME_HOURLY': 'Full Time (Hourly)',
        'PART_TIME': 'Part Time (Hourly)',
        'SEASONAL': 'Seasonal',
        'INPATRIATE': 'Inpatriate',
        'EXPATRIATE': 'Expatriate',
        'CONTRACTOR': 'Contractor',
        'VARIABLE': 'Variable',
        'TEMPORARY_FULL_TIME': 'Temporary Full Time',
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')
    employee_id = models.CharField(max_length=256)
    email = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=256, choices=STATUS_CHOICES, default='ACTIVE')
    type = models.CharField(max_length=256, choices=TYPE_CHOICES, default='PART_TIME')
    managed_teams = models.ManyToManyField(Team, related_name="managed_by", blank=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    effective_start_date = models.DateField()
    effective_end_date = models.DateField()
    def __str__(self):
        return str(self.skill.name)

class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    effective_date = models.DateField()
    monday = models.ManyToManyField("AvailabilityPeriod", related_name="monday")
    tuesday = models.ManyToManyField("AvailabilityPeriod", related_name="tuesday")
    wednesday = models.ManyToManyField("AvailabilityPeriod", related_name="wednesday")
    thursday = models.ManyToManyField("AvailabilityPeriod", related_name="thursday")
    friday = models.ManyToManyField("AvailabilityPeriod", related_name="friday")
    saturday = models.ManyToManyField("AvailabilityPeriod", related_name="saturday")
    sunday = models.ManyToManyField("AvailabilityPeriod", related_name="sunday")

    class Meta:
        verbose_name_plural = "Availabilities"


class AvailabilityPeriod(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)
