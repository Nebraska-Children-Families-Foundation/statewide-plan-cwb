from django.contrib import admin
from .models import (
    ActivityStatus, NcffTeam, CommunityCollaborative,
    ChangeIndicator, PerformanceMeasure, DhhsPriority,
    CommunityActionStep, NCActionStep, Strategy, Objective, Goal, SystemPartner, CollaborativeStrategyPriority,
    NcffTeamStrategyPriority, PartnerStrategyPriority, SystemPartnerCommitment
)


# Admin models

class CommunityActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_number', 'activity_name', 'activity_status', 'completedby_year', 'completedby_quarter',
                    'related_collaborative')
    search_fields = ('activity_name', 'activity_status')
    list_filter = ('related_collaborative', 'activity_status')

    readonly_fields = ('activity_number',)

    def get_community_collab(self, obj):
        return obj.related_collaborative.community_collab_name
    get_community_collab.short_description = 'Community Collaborative'


class CommunityCollaborativeAdmin(admin.ModelAdmin):
    list_display = ('community_collab_name', 'priority_strategy_count', 'community_activity_count')
    search_fields = ('community_collab_name', 'community_collab_short_name',)

    def priority_strategy_count(self, obj):
        return CollaborativeStrategyPriority.objects.filter(community_collaborative=obj).count()

    priority_strategy_count.short_description = 'Priority Strategies Count'

    def community_activity_count(self, obj):
        return CommunityActionStep.objects.filter(related_collaborative=obj).count()

    community_activity_count.short_description = 'Activity Count'


class CollaborativeStrategyPriorityInline(admin.TabularInline):
    # Specify the model that this inline admin will manage.
    model = CollaborativeStrategyPriority

    # Set the number of extra forms to display in the inline admin.
    # This allows for adding new StrategyPriority instances directly from the Strategy admin page.
    extra = 1

    # Set the names
    verbose_name = 'Collaborative Priority'
    verbose_name_plural = 'Collaborative Priorities'


class NcffTeamStrategyPriorityInline(admin.TabularInline):
    model = NcffTeamStrategyPriority
    extra = 1
    verbose_name = "NCFF Team Priority"
    verbose_name_plural = "NCFF Team Priorities"


class PartnerStrategyPriorityInline(admin.TabularInline):
    model = PartnerStrategyPriority
    extra = 1
    verbose_name = "State Partner Priority"
    verbose_name_plural = "State Partner Priorities"



class StrategyAdmin(admin.ModelAdmin):
    list_display = ('strategy_number', 'strategy_name', 'get_goal_number', 'get_objective_number',
                    'get_priority_collaboratives', 'get_ncff_team_priorities',
                    'get_state_partner_priorities')
    search_fields = ('strategy_name', 'get_priority_collaboratives')
    list_filter = ('related_goal', 'related_objective', 'strategy_number',)
    ordering = ('strategy_number', 'related_goal', 'related_objective')
    inlines = [CollaborativeStrategyPriorityInline, PartnerStrategyPriorityInline, NcffTeamStrategyPriorityInline]

    readonly_fields = ('strategy_number',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, CollaborativeStrategyPriority) and not instance.pk:
                # This is a new StrategyPriority instance being added
                instance.is_priority = True
            instance.save()
        formset.save_m2m()

    def get_priority_collaboratives(self, obj):
        return ", ".join([csp.community_collaborative.community_collab_name for csp in
                          obj.collaborativestrategypriority_set.filter(is_priority=True)])

    get_priority_collaboratives.short_description = 'Collab Designated Priority'

    def get_ncff_team_priorities(self, obj):
        return ", ".join([team.ncff_team_name for team in obj.ncffteamstrategypriority_set.filter(is_priority=True)])

    get_ncff_team_priorities.short_description = 'NCFF Team Priorities'

    def get_state_partner_priorities(self, obj):
        return ", ".join(
            [partner.system_partner_name for partner in obj.partnerstrategypriority_set.filter(is_priority=True)])

    get_state_partner_priorities.short_description = 'State Partner Priorities'

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


# class DhhsPriorityAdmin(admin.ModelAdmin):
#     list_display = ('priority_description', 'related_goal')
#     search_fields = ('priority_description',)
#
#     def get_goal_number(self, obj):
#         return obj.related_goal.goal_number
#     get_goal_number.short_description = 'Goal Number'


class SystemPartnerCommitmentAdmin(admin.ModelAdmin):
    list_display = ('commitment_number', 'commitment_name', 'commitment_status', 'completedby_year', 'completedby_quarter',
                    'related_systempartner', 'get_related_goal_number', 'get_related_objective_number', 'get_related_strategy_number')
    search_fields = ('commitment_name', 'commitment_details', 'commitment_lead')
    list_filter = ('commitment_status', 'related_systempartner', 'related_goal', 'related_objective', 'related_strategy')

    readonly_fields = ('commitment_number',)

    def get_related_goal_number(self, obj):
        return obj.related_goal.goal_number
    get_related_goal_number.short_description = 'Goal Number'

    def get_related_objective_number(self, obj):
        return obj.related_objective.objective_number
    get_related_objective_number.short_description = 'Objective Number'

    def get_related_strategy_number(self, obj):
        return obj.related_strategy.strategy_number
    get_related_strategy_number.short_description = 'Strategy Number'


class StrategyActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_number', 'activity_name', 'activity_status', 'completedby_year', 'completedby_quarter')
    search_fields = ('activity_name', 'activity_status')

    readonly_fields = ('activity_number',)


class StrategyPriorityAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'community_collab')
    search_fields = ('strategy', 'community_collab')


# Register your models here
admin.site.register(CommunityActionStep, CommunityActivityAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Objective, ObjectiveAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(NcffTeam, NcffTeamAdmin)
admin.site.register(PerformanceMeasure, PerformanceMeasureAdmin)
admin.site.register(ChangeIndicator, ChangeIndicatorAdmin)
admin.site.register(NCActionStep, StrategyActivityAdmin)
# admin.site.register(DhhsPriority, DhhsPriorityAdmin)
admin.site.register(SystemPartnerCommitment, SystemPartnerCommitmentAdmin)
admin.site.register(SystemPartner, SystemPartnerAdmin)
admin.site.register(NcffTeamStrategyPriority)
admin.site.register(PartnerStrategyPriority)
