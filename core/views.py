from django.shortcuts import render
from .models import Goal, Objective, Strategy


def home(request):
    goals = Goal.objects.all().prefetch_related('objective_set__strategy_set')
    context = {'goals': goals}
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def communication_plan(request):
    return render(request, 'core/communication-plan.html')


def community_activities(request):
    return render(request, 'core/community-activities.html')


def partner_activities(request):
    return render(request, 'core/partner-activities.html')


def community_collaboratives(request):
    return render(request, 'core/community-collaboratives.html')


def strategies_objectives(request):
    return render(request, 'core/strategies-objectives.html')


def goals(request):
    return render(request, 'core/goals.html')


def activities(request):
    return render(request, 'core/activities.html')