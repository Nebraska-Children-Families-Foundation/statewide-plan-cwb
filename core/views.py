from django.shortcuts import render, redirect, get_object_or_404
from .models import (Goal, Objective, Strategy, CommunityActionStep, NCActionStep, CommunityCollaborative, NcffTeam,
                     SystemPartner, CollaborativeStrategyPriority)
from .forms import CommunityActivityForm, PartnerActivityForm, NcffActivityForm
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from .permissions import has_edit_permission, has_commitment_edit_permission
from .plan_work.models import SystemPartnerCommitment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import AppUser
from django.db.models import Count


def home(request):
    goals = Goal.objects.all().prefetch_related('objective_set__strategy_set')
    context = {'goals': goals}
    return render(request, 'core/home.html', context)

def privacy(request):
    return render(request, 'core/privacy.html')


def terms_of_use(request):
    return render(request, 'core/terms-of-use.html')


def about(request):
    return render(request, 'core/about.html')


def communication_plan(request):
    return render(request, 'core/communication-plan.html')

def reports(request):
    return render(request, 'core/reports.html')


@login_required
def create_strategy(request):
    return render(request, 'core/create-strategy.html')


def community_activities(request, strategy_id):
    strategy = get_object_or_404(Strategy, pk=strategy_id)
    objective = strategy.related_objective
    goal = objective.related_goal
    activities = CommunityActionStep.objects.filter(related_strategy=strategy_id)
    collaboratives = CommunityCollaborative.objects.all()
    return render(request, 'core/community-activities.html', {
        'activities': activities,
        'collaboratives': collaboratives,
        'goal': goal,
        'objective': objective,
        'strategy': strategy
    })


def partner_activities(request, strategy_id=None):
    activities = SystemPartnerCommitment.objects.filter(related_strategy=strategy_id)
    return render(request, 'core/partner-activities.html', {'activities': activities})


def nc_activities(request, strategy_id):
    activities = NCActionStep.objects.filter(related_strategy=strategy_id)
    return render(request, 'core/nc-activities.html', {'activities': activities})


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

@login_required
def create_community_activity(request):
    if request.method == 'POST':
        form = CommunityActivityForm(request.POST)
        if form.is_valid():
            community_activity = form.save(commit=False)
            community_activity.community_creator = request.user  # Set the creator to the current user
            community_activity.save()
            return redirect('it_worked')  # Ensure this redirects to an appropriate confirmation or success page
    else:
        form = CommunityActivityForm()
    return render(request, 'core/create-community-activity.html', {'form': form})



@login_required
def create_partner_commitment(request):
    if request.method == 'POST':
        form = PartnerActivityForm(request.POST)
        if form.is_valid():
            commitment = form.save(commit=False)
            if not commitment.commitment_number:
                prefix = "COMMIT-"
                last_commitment = SystemPartnerCommitment.objects.order_by('-commitment_number').last()
                new_number = 1000  # Start from 1000
                if last_commitment:
                    number_part = last_commitment.commitment_number.split('-')[2]
                    new_number = int(number_part) + 1
                commitment.commitment_number = f"{prefix}{new_number}"
            commitment.system_partner_creator = request.user
            commitment.save()
            messages.success(request, 'Your commitment has been recorded.')
            return redirect('it_worked')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PartnerActivityForm()
    return render(request, 'core/create-partner-activity.html', {'form': form})


@login_required
def create_nc_activity(request):
    if request.method == 'POST':
        form = NcffActivityForm(request.POST)
        if form.is_valid():
            nc_activity = form.save(commit=False)
            nc_activity.nc_staff_creator = request.user
            nc_activity.save()
            messages.success(request, 'NC Activity has been successfully created.')
            # Use 'strategy_id' instead of 'id' for the primary key attribute
            return redirect('nc_activities', strategy_id=nc_activity.related_strategy.strategy_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = NcffActivityForm()
    return render(request, 'core/create-nc-action-step.html', {'form': form})


# For the dynamic chaining for dropdowns of Goals and Objectives
def load_objectives(request):
    goal_id = request.GET.get('goal_id')
    objectives = Objective.objects.filter(goal_id=goal_id).order_by('name')
    return JsonResponse(list(objectives.values('id', 'name')), safe=False)


@login_required
def update_nc_activity(request, pk):
    activity = get_object_or_404(NCActionStep, pk=pk)
    if not activity.nc_staff_creator == request.user:
        return HttpResponseForbidden("You do not have permission to edit this action step.")

    if request.method == 'POST':
        form = NcffActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('nc_activities', strategy_id=activity.related_strategy.pk)
    else:
        form = NcffActivityForm(instance=activity)

    return render(request, 'core/edit-nc-activity.html', {'form': form})


@login_required
def update_community_activity(request, pk):
    activity = get_object_or_404(CommunityActionStep, pk=pk)
    if not has_edit_permission(request.user, activity):
        return HttpResponseForbidden("You do not have permission to edit this action step.")

    if request.method == 'POST':
        form = CommunityActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('community_activities', strategy_id=activity.related_strategy.pk)
    else:
        form = CommunityActivityForm(instance=activity)

    return render(request, 'core/update-community-activity.html', {'form': form})


@login_required
def update_system_partner_commitment(request, pk):
    commitment = get_object_or_404(SystemPartnerCommitment, pk=pk)
    if not commitment.system_partner_creator == request.user:
        return HttpResponseForbidden("You do not have permission to edit this commitment.")

    if request.method == 'POST':
        form = PartnerActivityForm(request.POST, instance=commitment)
        if form.is_valid():
            form.save()
            return redirect('partner_activities', strategy_id=commitment.related_strategy.pk)
    else:
        form = PartnerActivityForm(instance=commitment)

    return render(request, 'core/edit-system-partner-commitment.html', {'form': form})


@login_required
def individual_dashboard(request):
    user = request.user
    activities_count = {
        'total': 0,
        'not_started': 0,
        'in_progress': 0,
        'completed': 0,
        'ongoing': 0,
    }
    activities = []

    if user.member_type == AppUser.MemberTypes.COMMUNITY_COLLABORATIVE:
        activities = CommunityActionStep.objects.filter(community_creator=user)
    elif user.member_type == AppUser.MemberTypes.NCFF_TEAM:
        activities = NCActionStep.objects.filter(nc_staff_creator=user)
    elif user.member_type == AppUser.MemberTypes.SYSTEM_PARTNER:
        activities = SystemPartnerCommitment.objects.filter(system_partner_creator=user)

    activities_count['total'] = activities.count()
    activities_count['not_started'] = activities.filter(activity_status='Not Started').count()
    activities_count['in_progress'] = activities.filter(activity_status='In Progress').count()
    activities_count['completed'] = activities.filter(activity_status='Completed').count()
    activities_count['ongoing'] = activities.filter(activity_status='Ongoing').count()

    context = {
        'activities_count': activities_count,
        'activities': activities
    }
    return render(request, 'core/individual-dashboard.html', context)


@login_required
def activity_details(request, activity_id):
    user = request.user
    activity = None
    activity_type = None

    if user.member_type == AppUser.MemberTypes.COMMUNITY_COLLABORATIVE:
        activity = get_object_or_404(CommunityActionStep, activity_id=activity_id)
        activity_type = 'community'
    elif user.member_type == AppUser.MemberTypes.NCFF_TEAM:
        activity = get_object_or_404(NCActionStep, activity_id=activity_id)
        activity_type = 'nc'
    elif user.member_type == AppUser.MemberTypes.SYSTEM_PARTNER:
        activity = get_object_or_404(SystemPartnerCommitment, commitment_id=activity_id)
        activity_type = 'partner'

    context = {
        'activity': activity,
        'activity_type': activity_type
    }
    return render(request, 'core/activity-details.html', context)


def it_worked(request):
    return render(request, 'core/it-worked.html')
