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
from .standardization import Years, Quarters, ActivityStatusChoice


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
    activities = CommunityActionStep.objects.filter(related_strategy=strategy_id)
    collaboratives = CommunityCollaborative.objects.all()
    return render(request, 'core/community-activities.html', {'activities': activities,
                                                              'collaboratives': collaboratives})


def partner_activities(request, strategy_id=None):
    activities = SystemPartnerCommitment.objects.filter(related_strategy=strategy_id)
    return render(request, 'core/partner-activities.html', {'activities': activities})


def nc_activities(request, strategy_id):
    activities = NCActionStep.objects.filter(related_strategy=strategy_id)
    return render(request, 'core/nc-activities.html', {'activities': activities})


def community_collaboratives(request):
    return render(request, 'core/community-collaboratives.html')


def strategies_objectives(request):
    goals = Goal.objects.prefetch_related('objective_set').all()
    return render(request, 'core/strategies-objectives.html', {'goals': goals})


def goals(request):
    goals = Goal.objects.prefetch_related('changeindicator_set', 'performancemeasure_set', 'objective_set').all()
    return render(request, 'core/goals.html', {'goals': goals})


def strategies(request, objective_id):
    objective = Objective.objects.get(objective_id=objective_id)
    strategies = Strategy.objects.filter(related_objective=objective)
    return render(request, 'core/strategies.html', {'strategies': strategies, 'objective': objective})


def activities(request):
    return render(request, 'core/activities.html')


# views.py

@login_required
def action_steps_view(request):
    """
    Main view for action steps filtering interface
    """
    user = request.user
    initial_actor_type = None

    # Set initial actor type based on user's member type
    if user.member_type == AppUser.MemberTypes.NCFF_TEAM:
        initial_actor_type = 'nc'
    elif user.member_type == AppUser.MemberTypes.COMMUNITY_COLLABORATIVE:
        initial_actor_type = 'community'
    elif user.member_type == AppUser.MemberTypes.SYSTEM_PARTNER:
        initial_actor_type = 'partner'

    form = ActionStepsFilterForm()

    context = {
        'form': form,
        'actor_type': initial_actor_type,
        'goals': Goal.objects.all().order_by('goal_number'),
        'years': Years.choices,
        'quarters': Quarters.choices,
        'statuses': ActivityStatusChoice.choices,
    }

    return render(request, 'core/action_steps.html', context)


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
                last_commitment = SystemPartnerCommitment.objects.filter(commitment_number__startswith=prefix).order_by('-commitment_number').first()
                new_number = 1000  # Start from 1000
                if last_commitment and last_commitment.commitment_number:
                    parts = last_commitment.commitment_number.split('-')
                    if len(parts) >= 3 and parts[2].isdigit():
                        last_number = int(parts[2])
                        new_number = last_number + 1
                    else:
                        new_number = 1000  # Fallback
                else:
                    new_number = 1000  # Start from 1000 if no last commitment
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


def update_community_activity(request, pk):
    activity = get_object_or_404(CommunityActionStep, pk=pk)
    if not has_edit_permission(request.user, activity):
        return HttpResponseForbidden("You do not have permission to edit this action step.")

    if request.method == 'POST':
        form = CommunityActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            # Redirect to a success page
            return redirect('some-success-url')
    else:
        form = CommunityActivityForm(instance=activity)

    return render(request, 'core/update-community-activity.html', {'form': form})


def update_system_partner_commitment(request, pk):
    commitment = get_object_or_404(SystemPartnerCommitment, pk=pk)
    if not has_commitment_edit_permission(request.user, commitment):
        return HttpResponseForbidden("You do not have permission to edit this commitment.")

    if request.method == 'POST':
        form = PartnerActivityForm(request.POST, instance=commitment)
        if form.is_valid():
            form.save()
            return redirect('commitment-detail-view', pk=commitment.pk)  # Redirect to the commitment's detail view or another appropriate page
    else:
        form = PartnerActivityForm(instance=commitment)

    return render(request, 'core/update-system-partner-commitment.html', {'form': form})


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

    if user.member_type == AppUser.MemberTypes.COMMUNITY_COLLABORATIVE:
        activity = get_object_or_404(CommunityActionStep, activity_id=activity_id)
    elif user.member_type == AppUser.MemberTypes.NCFF_TEAM:
        activity = get_object_or_404(NCActionStep, activity_id=activity_id)
    elif user.member_type == AppUser.MemberTypes.SYSTEM_PARTNER:
        activity = get_object_or_404(SystemPartnerCommitment, commitment_id=activity_id)

    context = {
        'activity': activity
    }
    return render(request, 'core/activity-details.html', context)


def clean(self):
    cleaned_data = super().clean()
    if not cleaned_data.get('related_goal'):
        raise forms.ValidationError("Related Goal is required.")
    if not cleaned_data.get('related_objective'):
        raise forms.ValidationError("Related Objective is required.")
    if not cleaned_data.get('related_strategy'):
        raise forms.ValidationError("Related Strategy is required.")
    return cleaned_data


def it_worked(request):
    return render(request, 'core/it-worked.html')


@login_required
def set_collaborative_priorities(request):
    # Ensure user is associated with a collaborative
    if not request.user.community_collaborative:
        messages.error(request, "You must be associated with a Community Collaborative to access this page.")
        return redirect('home')

    collaborative = request.user.community_collaborative

    # Get all strategies and mark which ones are priorities
    strategies = Strategy.objects.all().select_related(
        'related_goal',
        'related_objective'
    ).prefetch_related(
        'collaborativestrategypriority_set'
    )

    # Mark which strategies are priorities for this collaborative
    for strategy in strategies:
        strategy.is_priority = strategy.collaborativestrategypriority_set.filter(
            community_collaborative=collaborative,
            is_priority=True
        ).exists()

    if request.method == 'POST':
        # Get the list of selected strategy IDs
        selected_strategies = request.POST.getlist('priority_strategies')

        # Update priorities
        # First, set all existing priorities to False
        CollaborativeStrategyPriority.objects.filter(
            community_collaborative=collaborative
        ).update(is_priority=False)

        # Then set selected ones to True
        for strategy_id in selected_strategies:
            CollaborativeStrategyPriority.objects.update_or_create(
                community_collaborative=collaborative,
                strategy_id=strategy_id,
                defaults={'is_priority': True}
            )

        messages.success(request, "Strategy priorities have been updated successfully.")
        return redirect('set_collaborative_priorities')

    context = {
        'strategies': strategies,
        'community_collab_name': collaborative.community_collab_name
    }

    return render(request, 'core/set_collaborative_priorities.html', context)