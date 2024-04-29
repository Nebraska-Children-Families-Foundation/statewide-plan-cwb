def has_edit_permission(user, action_step):
    # Check if the user is the creator
    if action_step.creator == user:
        return True
    # Check if the user is part of the same collaborative linked to the action step
    if user.community_collaborative == action_step.related_collaborative:
        return True
    return False
