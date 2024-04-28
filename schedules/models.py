from django.db import models

from employees.models import Employee
from forecast.models import Position
from teams.models import Organization, Team


class SchedulePeriod(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.organization} | {self.start_date} - {self.end_date}'


class Schedule(models.Model):
    STAGE_CHOICES = {
        'FORECASTED': 'Forecasted',
        'DRAFT': 'Draft',
        'IN_REVIEW': 'In Review',
        'PUBLISHED': 'Published',
    }
    period = models.ForeignKey(SchedulePeriod, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='FORECASTED')


class Shift(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.position.name} | {self.start_date} - ({self.start_time}-{self.end_time})'

