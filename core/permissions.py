# core/permissions.py
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden


def has_community_action_step_edit_permission(user, action_step):
    """
    Check if user can edit a CommunityActionStep
    Returns True if:
    1. User is superuser
    2. User is NCFF Team Member (can edit all action steps)
    3. User is the creator of the action step
    4. User belongs to the same collaborative as the action step
    """
    if user.is_superuser:
        return True

    # NCFF Team Members can edit all Community Action Steps
    if user.member_type == user.MemberTypes.NCFF_TEAM:
        return True

    # Check if the user is the creator
    if action_step.community_creator == user:
        return True

    # Check if the user is part of the same collaborative
    if (user.member_type == user.MemberTypes.COMMUNITY_COLLABORATIVE and
            user.community_collaborative == action_step.related_collaborative):
        return True

    return False


def require_community_action_step_edit_permission(view_func):
    """
    Decorator to check edit permissions for CommunityActionStep
    Usage: @require_community_action_step_edit_permission
    """

    @wraps(view_func)
    def wrapper(request, activity_id, *args, **kwargs):
        from core.plan_work.models import CommunityActionStep

        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to edit action steps.")

        action_step = get_object_or_404(CommunityActionStep, activity_id=activity_id)

        if not has_community_action_step_edit_permission(request.user, action_step):
            return HttpResponseForbidden("You don't have permission to edit this action step.")

        # Pass the action_step to the view to avoid re-fetching
        return view_func(request, action_step, *args, **kwargs)

    return wrapper


def has_edit_permission(user, action_step):
    """Legacy function - keeping for backward compatibility"""
    return has_community_action_step_edit_permission(user, action_step)


def has_commitment_edit_permission(user, commitment):
    """Check if user can edit a SystemPartnerCommitment"""
    if user.is_superuser:
        return True

    # Check if the user is the creator
    if commitment.system_partner_creator == user:
        return True

    # Check if the user belongs to the System Partner associated with the commitment
    if (user.member_type == user.MemberTypes.SYSTEM_PARTNER and
            user.system_partner == commitment.related_systempartner):
        return True

    return False