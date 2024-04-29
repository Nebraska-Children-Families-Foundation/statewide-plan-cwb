from django.shortcuts import render, redirect
from .models import (Goal, Objective, Strategy, CommunityActionStep, NCActionStep, CommunityCollaborative, NcffTeam,
                     SystemPartner, CollaborativeStrategyPriority)
from .forms import CommunityActivityForm, PartnerActivityForm
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView


def home(request):
    goals = Goal.objects.all().prefetch_related('objective_set__strategy_set')
    context = {'goals': goals}
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def communication_plan(request):
    return render(request, 'core/communication-plan.html')


def community_activities(request, strategy_id):
    activities = CommunityActionStep.objects.filter(related_strategy=strategy_id)
    collaboratives = CommunityCollaborative.objects.all()
    return render(request, 'core/community-activities.html', {'activities': activities,
                                                              'collaboratives': collaboratives})


def partner_activities(request, strategy_id=None):
    activities = NCActionStep.objects.filter(related_strategy=strategy_id)
    return render(request, 'core/partner-activities.html', {'activities': activities})


def community_collaboratives(request):
    return render(request, 'core/community-collaboratives.html')


def strategies_objectives(request):
    return render(request, 'core/strategies-objectives.html')


def goals(request):
    goals = Goal.objects.prefetch_related('changeindicator_set', 'performancemeasure_set', 'objective_set').all()
    return render(request, 'core/goals.html', {'goals': goals})


def strategies(request, objective_id):
    objective = Objective.objects.get(objective_id=objective_id)
    strategies = Strategy.objects.filter(related_objective=objective)
    return render(request, 'core/strategies.html', {'strategies': strategies, 'objective': objective})


def activities(request):
    return render(request, 'core/activities.html')


def strategy_list(request):
    # Fetching initial data for dropdowns
    goals = Goal.objects.all()
    ncff_teams = NcffTeam.objects.all()
    system_partners = SystemPartner.objects.all()
    community_collaboratives = CommunityCollaborative.objects.all()

    # Fetching strategies and related data
    strategies = Strategy.objects.prefetch_related('ncff_teams', 'system_partners', 'community_collaboratives').all()

    # Prepare additional data for each strategy
    for strategy in strategies:
        # Fetching Community Collaboratives that marked the strategy as a priority
        strategy.priority_collaboratives = CollaborativeStrategyPriority.objects.filter(
            strategy=strategy, is_priority=True
        ).select_related('community_collaborative')

        # Count of Partner and Community Activities
        strategy.partner_activities_count = NCActionStep.objects.filter(related_strategy=strategy).count()
        strategy.community_activities_count = CommunityActionStep.objects.filter(related_strategy=strategy).count()

    context = {
        'goals': goals,
        'ncff_teams': ncff_teams,
        'system_partners': system_partners,
        'strategies': strategies,
        'community_collaboratives': community_collaboratives,
    }
    return render(request, 'core/strategy-list.html', context)


def create_community_activity(request):
    if request.method == 'POST':
        form = CommunityActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core/create-community-activity.html')
    else:
        form = CommunityActivityForm()
    return render(request, 'core/create-community-activity.html', {'form': form})


def create_partner_activity(request):
    if request.method == 'POST':
        form = PartnerActivityForm(request.Post)
        if form.is_valid():
            form.save()
            return redirect('core/create-partner-activity.html')
    else:
        form = PartnerActivityForm()
    return render(request, 'core/create-partner-activity.html', {'form': form})


# For the dynamic chaining for dropdowns of Goals and Objectives
def load_objectives(request):
    goal_id = request.GET.get('goal_id')
    objectives = Objective.objects.filter(goal_id=goal_id).order_by('name')
    return JsonResponse(list(objectives.values('id', 'name')), safe=False)


class CommunityActionStepUpdateView(UpdateView):
    model = CommunityActionStep
    fields = ['activity_name', 'activity_details', 'activity_status', 'completedby_year', 'completedby_quarter']
    template_name = 'your_template.html'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.has_edit_permission(request.user, obj):
            return HttpResponseForbidden("You do not have permission to edit this action step.")
        return super().dispatch(request, *args, **kwargs)

    def has_edit_permission(self, user, action_step):
        # Check if the user is the creator
        if action_step.creator == user:
            return True
        # Check if the user is part of the same collaborative
        if user.community_collaborative == action_step.related_collaborative:
            return True
        return False
