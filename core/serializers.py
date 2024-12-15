from rest_framework import serializers
from .models import NCActionStep, CommunityActionStep, SystemPartnerCommitment
from django.urls import reverse


class NCActionStepSerializer(serializers.ModelSerializer):
    goal = serializers.SerializerMethodField()
    objective = serializers.SerializerMethodField()
    strategy = serializers.SerializerMethodField()
    actor_type = serializers.SerializerMethodField()
    actor_name = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = NCActionStep
        fields = ['activity_id', 'activity_number', 'activity_name', 'activity_details',
                 'activity_status', 'completedby_year', 'completedby_quarter',
                 'goal', 'objective', 'strategy', 'actor_type', 'actor_name', 'view_url']

    def get_goal(self, obj):
        return f"Goal {obj.related_goal.goal_number}" if obj.related_goal else "N/A"

    def get_objective(self, obj):
        return f"Obj {obj.related_objective.objective_number}" if obj.related_objective else "N/A"

    def get_strategy(self, obj):
        return obj.related_strategy.strategy_number if obj.related_strategy else "N/A"

    def get_actor_type(self, obj):
        return "Nebraska Children"

    def get_actor_name(self, obj):
        return str(obj.ncff_team) if obj.ncff_team else "N/A"

    def get_view_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('activity_details', kwargs={'activity_id': obj.activity_id})
            )
        return None


class CommunityActionStepSerializer(serializers.ModelSerializer):
    goal = serializers.SerializerMethodField()
    objective = serializers.SerializerMethodField()
    strategy = serializers.SerializerMethodField()
    actor_type = serializers.SerializerMethodField()
    actor_name = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = CommunityActionStep
        fields = ['activity_id', 'activity_number', 'activity_name', 'activity_details',
                 'activity_status', 'completedby_year', 'completedby_quarter',
                 'goal', 'objective', 'strategy', 'actor_type', 'actor_name', 'view_url']

    def get_goal(self, obj):
        return f"Goal {obj.related_goal.goal_number}" if obj.related_goal else "N/A"

    def get_objective(self, obj):
        return f"Obj {obj.related_objective.objective_number}" if obj.related_objective else "N/A"

    def get_strategy(self, obj):
        return obj.related_strategy.strategy_number if obj.related_strategy else "N/A"

    def get_actor_type(self, obj):
        return "Community Collaborative"

    def get_actor_name(self, obj):
        return str(obj.related_collaborative) if obj.related_collaborative else "N/A"

    def get_view_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('activity_details', kwargs={'activity_id': obj.activity_id})
            )
        return None


class SystemPartnerCommitmentSerializer(serializers.ModelSerializer):
    goal = serializers.SerializerMethodField()
    objective = serializers.SerializerMethodField()
    strategy = serializers.SerializerMethodField()
    actor_type = serializers.SerializerMethodField()
    actor_name = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = SystemPartnerCommitment
        fields = ['commitment_id', 'commitment_number', 'commitment_name', 'commitment_details',
                 'commitment_status', 'completedby_year', 'completedby_quarter',
                 'goal', 'objective', 'strategy', 'actor_type', 'actor_name', 'view_url']

    def get_goal(self, obj):
        return f"Goal {obj.related_goal.goal_number}" if obj.related_goal else "N/A"

    def get_objective(self, obj):
        return f"Obj {obj.related_objective.objective_number}" if obj.related_objective else "N/A"

    def get_strategy(self, obj):
        return obj.related_strategy.strategy_number if obj.related_strategy else "N/A"

    def get_actor_type(self, obj):
        return "System Partner"

    def get_actor_name(self, obj):
        return str(obj.related_systempartner) if obj.related_systempartner else "N/A"

    def get_view_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('activity_details', kwargs={'activity_id': obj.commitment_id})
            )
        return None
