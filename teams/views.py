from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Team
from employees.models import Employee
from .forms import TeamForm

@login_required
def index(request):
    context = {}
    
    context["teams"] = Team.objects.all()
    context["employee"] = Employee.objects.get(user=request.user)
    defined = Employee.objects.get(user=request.user).managed_teams.all()
    all = []
    for team in defined:
        if not team in all:
            all += team.get_descendants(include_self=True)
    context["managed"] = all

    return render(request, "list.html", context)
