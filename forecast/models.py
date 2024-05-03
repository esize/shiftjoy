from django.db import models
from colorfield.fields import ColorField

class ForecastVariable(models.Model):
    TYPE_OPTIONS = {
        'VALUE': 'Value',
        'CALCULATED': 'Calculated',
        'OFFSET': 'Offset'
    }
    FREQUENCY_OPTIONS = {
        'DAILY': 'Daily',
        'SEGMENT': 'Segment'
    }
    FORMAT_OPTIONS = {
        "TIME": 'Time',
        "TEXT": 'Text',
        "NUMBER": 'Number'
    }
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default=TYPE_OPTIONS['VALUE'])
    frequency = models.CharField(max_length=10, choices=FREQUENCY_OPTIONS, default=FREQUENCY_OPTIONS['DAILY'])
    format = models.CharField(max_length=64, choices=FORMAT_OPTIONS, default=FORMAT_OPTIONS['TIME'])
    default_value = models.CharField(max_length=64, null=True, blank=True)
    calculated_default_value = models.ForeignKey('CalculatedValue', on_delete=models.SET_NULL, null=True, blank=True)
    offset_linked_variable = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    offset_days = models.IntegerField(null=True, blank=True)
    offset_hours = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey("teams.Location", on_delete=models.SET_NULL, null=True, blank=True)
    behaviors = models.ManyToManyField("VariableBehavior", blank=True)

    def __str__(self):
        if not self.active:
            return "(Disabled) " + self.name + " - " + self.type
        return self.name + " - " + self.type


class CalculatedValue(models.Model):
    OPERATOR_VALUES = {
        "ADD": '+',
        "SUB": '-',
    }
    variable = models.ForeignKey(ForecastVariable, on_delete=models.SET_NULL, null=True, blank=True, related_name='calculated_values')
    operator = models.CharField(max_length=10, choices=OPERATOR_VALUES, default=OPERATOR_VALUES['ADD'])
    value = models.CharField(max_length=64, null=True, blank=True)
    value_variable = models.ForeignKey(ForecastVariable, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.value_variable is not None:
            return str(self.variable.name) + self.operator + str(self.value_variable.name)
        return str(self.variable.name) + self.operator + str(self.value)


class Condition(models.Model):
    COMPARISON_OPERATOR_OPTIONS = {
        "LT": '<',
        "LE": "≤",
        "GT": '>',
        "GE": "≥",
        "EQ": '=',
        "NE": '≠'
    }
    variable = models.ForeignKey(ForecastVariable, on_delete=models.CASCADE, related_name='conditions_referencing_as_variable')
    comparison_operator = models.CharField(max_length=2, choices=COMPARISON_OPERATOR_OPTIONS, default='>')
    comparison_variable = models.ForeignKey(ForecastVariable, on_delete=models.CASCADE, null=True, blank=True, related_name='conditions_referencing_as_comparison_variable')
    comparison_value = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        if self.comparison_variable is not None:
            return str(self.variable.name) + self.comparison_operator + str(self.comparison_variable.name)
        return str(self.variable.name) + self.comparison_operator + str(self.comparison_value)


class VariableBehavior(models.Model):
    name = models.CharField(max_length=100)
    conditions = models.ManyToManyField(Condition)
    value = models.CharField(max_length=64, null=True, blank=True)
    value_variable = models.ForeignKey(ForecastVariable, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class VariableInstance(models.Model):
    SEGMENT_OPTIONS = {
        '0000': '00:00',
        '0015': '00:15',
        '0030': '00:30',
        '0045': '00:45',
        '0100': '01:00',
        '0115': '01:15',
        '0130': '01:30',
        '0145': '01:45',
        '0200': '02:00',
        '0215': '02:15',
        '0230': '02:30',
        '0245': '02:45',
        '0300': '03:00',
        '0315': '03:15',
        '0330': '03:30',
        '0345': '03:45',
        '0400': '04:00',
        '0415': '04:15',
        '0430': '04:30',
        '0445': '04:45',
        '0500': '05:00',
        '0515': '05:15',
        '0530': '05:30',
        '0545': '05:45',
        '0600': '06:00',
        '0615': '06:15',
        '0630': '06:30',
        '0645': '06:45',
        '0700': '07:00',
        '0715': '07:15',
        '0730': '07:30',
        '0745': '07:45',
        '0800': '08:00',
        '0815': '08:15',
        '0830': '08:30',
        '0845': '08:45',
        '0900': '09:00',
        '0915': '09:15',
        '0930': '09:30',
        '0945': '09:45',
        '1000': '10:00',
        '1015': '10:15',
        '1030': '10:30',
        '1045': '10:45',
        '1100': '11:00',
        '1115': '11:15',
        '1130': '11:30',
        '1145': '11:45',
        '1200': '12:00',
        '1215': '12:15',
        '1230': '12:30',
        '1245': '12:45',
        '1300': '13:00',
        '1315': '13:15',
        '1330': '13:30',
        '1345': '13:45',
        '1400': '14:00',
        '1415': '14:15',
        '1430': '14:30',
        '1445': '14:45',
        '1500': '15:00',
        '1515': '15:15',
        '1530': '15:30',
        '1545': '15:45',
        '1600': '16:00',
        '1615': '16:15',
        '1630': '16:30',
        '1645': '16:45',
        '1700': '17:00',
        '1715': '17:15',
        '1730': '17:30',
        '1745': '17:45',
        '1800': '18:00',
        '1815': '18:15',
        '1830': '18:30',
        '1845': '18:45',
        '1900': '19:00',
        '1915': '19:15',
        '1930': '19:30',
        '1945': '19:45',
        '2000': '20:00',
        '2015': '20:15',
        '2030': '20:30',
        '2045': '20:45',
        '2100': '21:00',
        '2115': '21:15',
        '2130': '21:30',
        '2145': '21:45',
        '2200': '22:00',
        '2215': '22:15',
        '2230': '22:30',
        '2245': '22:45',
        '2300': '23:00',
        '2315': '23:15',
        '2330': '23:30',
        '2345': '23:45'
    }
    variable = models.ForeignKey(ForecastVariable, on_delete=models.CASCADE)
    value = models.CharField(max_length=64)
    date = models.DateField(auto_now=False, auto_now_add=False)
    segment = models.CharField(max_length=64, null=True, blank=True, choices=SEGMENT_OPTIONS)

    def __str__(self):
        if self.segment is not None:
            return self.variable.name + ' - ' + self.date.__format__("%d/%m/%Y") + ' (' + self.segment + ")"
        return self.variable.name + " - " + self.date.__format__("%d/%m/%Y")


class Skill(models.Model):
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)

    def __str__(self):
        if not self.active:
            return "(Disabled) " + self.name
        return self.name


class PositionBehavior(models.Model):
    OPERATOR_VALUES = {
        "ADD": '+',
        "SUB": '-',
    }
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    conditions = models.ManyToManyField(Condition)
    start_time_variable = models.ForeignKey(ForecastVariable, on_delete=models.CASCADE, related_name='start_time_variable')
    start_time_operator = models.CharField(max_length=64, choices=OPERATOR_VALUES)
    start_time_calc_value = models.CharField(max_length=64)
    end_time_variable = models.ForeignKey(ForecastVariable, on_delete=models.CASCADE, related_name='end_time_variable')
    end_time_operator = models.CharField(max_length=64, choices=OPERATOR_VALUES)
    end_time_calc_value = models.CharField(max_length=64)
    number_required = models.IntegerField(default=0)

    def __str__(self):
        if not self.active:
            return "(Disabled) " + self.name
        return self.name


class Position(models.Model):
    TYPE_CHOICES = {
        'FIXED': 'Fixed',
        'LIMIT': 'Limit',
        'SEGMENT': 'Segment'
    }
    GENDER_CHOICES = {
        'FEMALE': 'Female',
        'MALE': 'Male'
    }

    COLOR_PALETTE = [
        ('#000000', 'black'),
        ('#696969', 'dimgray'),
        ('#808080', 'gray'),
        ('#A9A9A9', 'darkgray'),
        ('#C0C0C0', 'silver'),
        ('#D3D3D3', 'lightgray'),
        ('#DCDCDC', 'gainsboro'),
        ('#FF0000', 'red'),
        ('#A52A2A', 'brown'),
        ('#FF4500', 'orangered'),
        ('#FFA500', 'orange'),
        ('#FFFF00', 'yellow'),
        ('#9ACD32', 'yellowgreen'),
        ('#008000', 'green'),
        ('#20B2AA', 'lightseagreen'),
        ('#00FFFF', 'aqua'),
        ('#00BFFF', 'deepskyblue'),
        ('#4169E1', 'royalblue'),
        ('#7B68EE', 'mediumslateblue'),
        ('#DA70D6', 'orchid')
    ]
    MINIMUM_AGE_CHOICES = {
        0: "No minimum age",
        16: "16 years old",
        18: "18 years old",
        21: "21 years old"
    }
    name = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE)
    color = ColorField(choices=COLOR_PALETTE)
    minimum_age = models.IntegerField(choices=MINIMUM_AGE_CHOICES)
    gender_specific = models.BooleanField(default=False)
    required_gender = models.CharField(max_length=64, null=True, blank=True, choices=GENDER_CHOICES)
    skills = models.ManyToManyField(Skill)
    behaviors = models.ManyToManyField(PositionBehavior)

    def __str__(self):
        if not self.active:
            return "(Disabled) " + self.name
        return self.name

