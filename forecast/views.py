from django.shortcuts import render
from .forms import PositionForm
from django.views.generic.edit import FormView

# Create your views here.
class PositionFormView(FormView):
    form_class=PositionForm
    template_name="positions.html"
    success_url='/'