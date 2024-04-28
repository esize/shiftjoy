from django.shortcuts import render
from .models import Team

def index(request):
    latest_team_list = Team.objects
