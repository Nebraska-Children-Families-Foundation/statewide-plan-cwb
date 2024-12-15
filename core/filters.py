import django_filters
from .models import NCActionStep, CommunityActionStep, SystemPartnerCommitment


class NCActionStepFilter(django_filters.FilterSet):
    class Meta:
        model = NCActionStep
        fields = {
            'ncff_team': ['exact'],
            'related_goal': ['exact'],
            'related_objective': ['exact'],
            'related_strategy': ['exact'],
            'activity_status': ['exact'],
            'completedby_year': ['exact'],
            'completedby_quarter': ['exact'],
        }


class CommunityActionStepFilter(django_filters.FilterSet):
    class Meta:
        model = CommunityActionStep
        fields = {
            'related_collaborative': ['exact'],
            'related_goal': ['exact'],
            'related_objective': ['exact'],
            'related_strategy': ['exact'],
            'activity_status': ['exact'],
            'completedby_year': ['exact'],
            'completedby_quarter': ['exact'],
        }


class SystemPartnerCommitmentFilter(django_filters.FilterSet):
    class Meta:
        model = SystemPartnerCommitment
        fields = {
            'related_systempartner': ['exact'],
            'related_goal': ['exact'],
            'related_objective': ['exact'],
            'related_strategy': ['exact'],
            'commitment_status': ['exact'],
            'completedby_year': ['exact'],
            'completedby_quarter': ['exact'],
        }