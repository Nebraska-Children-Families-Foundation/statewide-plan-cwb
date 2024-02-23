from django.shortcuts import render
from .models import Goal, Objective, Strategy

def home(request):
    goals = Goal.objects.all().prefetch_related('objective_set__strategy_set')
    context = {'goals': goals}
    return render(request, 'home.html', context)
