from django.forms import widgets
from django import forms

from .models import Position

class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = ['name', 'active', 'type', 'team', 'color', 'minimum_age', 'gender_specific', 'required_gender']
       