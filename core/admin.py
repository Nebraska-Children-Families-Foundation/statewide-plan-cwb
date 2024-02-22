from django.contrib import admin
from .models import (
    ActivityStatus, NcffTeam, CommunityCollaborative,
    ChangeIndicator, PerformanceMeasure, DhhsPriority,
    CommunityActivity, StrategyActivity, Strategy, Objective, Goal, SystemPartner
)


# Admin models

class CommunityActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'activity_status', 'completedby_year', 'completedby_quarter')
    search_fields = ('activity_name', 'activity_status')

    def get_community_collab(self, obj):
        return obj.related_collaborative.community_collab_name
    get_community_collab.short_description = 'Community Collaborative'


class CommunityCollaborativeAdmin(admin.ModelAdmin):
    list_display = ('community_collab_name',)
    search_fields = ('community_collab_name', 'community_collab_short_name',)


class StrategyAdmin(admin.ModelAdmin):
    list_display = ('strategy_name', 'get_goal_number', 'get_goal_name', 'get_objective_number', 'get_objective_name')
    search_fields = ('strategy_name',)
    list_filter = ('related_goal', 'related_objective', 'strategy_number',)

    def get_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_goal_number.short_description = 'Goal Number'

    def get_goal_name(self, obj):
        return obj.related_goal.goal_name
    get_goal_name.short_description = 'Goal Name'

    def get_objective_number(self, obj):
        return obj.related_objective.objective_number
    get_objective_number.short_description = 'Objective Number'

    def get_objective_name(self, obj):
        return obj.related_objective.objective_name
    get_objective_name.short_description = 'Objective Name'


class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('related_goal', 'objective_number', 'objective_name',)
    search_fields = ('objective_name',)
    list_filter = ('related_goal', 'objective_number',)

    def get_related_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_related_goal_number.short_description = 'Goal Number'

    def get_related_goal_name(self, obj):
        return obj.related_goal.goal_name
    get_related_goal_name.short_description = 'Goal Name'


class GoalAdmin(admin.ModelAdmin):
    list_display = ('goal_number', 'goal_name',)
    search_fields = ('goal_name',)
    ordering = ('goal_number',)


class ActivityStatusAdmin(admin.ModelAdmin):
    list_display = ('activity_status',)
    search_fields = ('activity_status',)


class NcffTeamAdmin(admin.ModelAdmin):
    list_display = ('ncff_team_name', 'strategy_count')
    search_fields = ('ncff_team_name',)

    def strategy_count(self, obj):  # Counts number of Strategies assigned to the team.
        return obj.strategy_set.count()
    strategy_count.short_description = '# of Strategies Assigned'


class SystemPartnerAdmin(admin.ModelAdmin):
    list_display = ('system_partner_name', 'system_partner_short_name', 'strategy_count',)
    search_fields = ('system_partner_name', 'system_partner_short_name',)
    ordering = ('system_partner_name',)

    def strategy_count(self, obj):  # Counts number of Strategies assigned to the partner.
        return obj.strategy_set.count()
    strategy_count.short_description = '# of Strategies Assigned'


class ChangeIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'related_goal')
    search_fields = ('indicator',)

    def get_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_goal_number.short_description = 'Goal Number'


class PerformanceMeasureAdmin(admin.ModelAdmin):
    list_display = ('measure', 'related_goal')
    search_fields = ('measure',)

    def get_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_goal_number.short_description = 'Goal Number'


class DhhsPriorityAdmin(admin.ModelAdmin):
    list_display = ('priority_description', 'related_goal')
    search_fields = ('priority_description',)

    def get_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_goal_number.short_description = 'Goal Number'


class StrategyActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_name', 'activity_status', 'completedby_year', 'completedby_quarter')
    search_fields = ('activity_name', 'activity_status')


class StrategyPriorityAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'community_collab')
    search_fields = ('strategy', 'community_collab')


# Register your models here
admin.site.register(CommunityActivity, CommunityActivityAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Objective, ObjectiveAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(NcffTeam, NcffTeamAdmin)
admin.site.register(CommunityCollaborative, CommunityCollaborativeAdmin)
admin.site.register(PerformanceMeasure, PerformanceMeasureAdmin)
admin.site.register(ChangeIndicator, ChangeIndicatorAdmin)
admin.site.register(StrategyActivity, StrategyActivityAdmin)
admin.site.register(DhhsPriority, DhhsPriorityAdmin)
admin.site.register(SystemPartner, SystemPartnerAdmin)
