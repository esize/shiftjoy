# Generated by Django 5.0.4 on 2024-05-03 06:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forecast', '0001_initial'),
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilityPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('employee_id', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=256)),
                ('date_of_birth', models.DateField()),
                ('status', models.CharField(choices=[('ONBOARDING', 'Onboarding'), ('ACTIVE', 'Active'), ('LEAVE', 'On Leave'), ('SUSPENDED', 'Suspended'), ('TERMINATED', 'Terminated')], default='ACTIVE', max_length=256)),
                ('type', models.CharField(choices=[('OFFICER', 'Officer'), ('FULL_TIME_SALARIED', 'Full Time (Salaried)'), ('FULL_TIME_HOURLY', 'Full Time (Hourly)'), ('PART_TIME', 'Part Time (Hourly)'), ('SEASONAL', 'Seasonal'), ('INPATRIATE', 'Inpatriate'), ('EXPATRIATE', 'Expatriate'), ('CONTRACTOR', 'Contractor'), ('VARIABLE', 'Variable'), ('TEMPORARY_FULL_TIME', 'Temporary Full Time')], default='PART_TIME', max_length=256)),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
                ('managed_teams', models.ManyToManyField(related_name='managed_by', to='teams.team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('effective_date', models.DateField()),
                ('friday', models.ManyToManyField(related_name='friday', to='employees.availabilityperiod')),
                ('monday', models.ManyToManyField(related_name='monday', to='employees.availabilityperiod')),
                ('saturday', models.ManyToManyField(related_name='saturday', to='employees.availabilityperiod')),
                ('sunday', models.ManyToManyField(related_name='sunday', to='employees.availabilityperiod')),
                ('thursday', models.ManyToManyField(related_name='thursday', to='employees.availabilityperiod')),
                ('tuesday', models.ManyToManyField(related_name='tuesday', to='employees.availabilityperiod')),
                ('wednesday', models.ManyToManyField(related_name='wednesday', to='employees.availabilityperiod')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
            ],
            options={
                'verbose_name_plural': 'Availabilities',
            },
        ),
        migrations.CreateModel(
            name='EmployeeSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('effective_start_date', models.DateField()),
                ('effective_end_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.skill')),
            ],
        ),
    ]
