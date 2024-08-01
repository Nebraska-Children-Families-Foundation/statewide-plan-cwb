def has_edit_permission(user, action_step):
    # Check if the user is the creator
    if action_step.community_creator == user:
        return True
    # Check if the user is part of the same collaborative linked to the action step
    if user.community_collaborative == action_step.related_collaborative:
        return True
    return False

def has_commitment_edit_permission(user, commitment):
    # Check if the user belongs to the System Partner associated with the commitment
    return user.system_partner == commitment.related_systempartner
