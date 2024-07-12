from django.contrib import admin
from core.admin.planactors_admin import CollaborativeStrategyPriorityInline, PartnerStrategyPriorityInline, \
    NcffTeamStrategyPriorityInline
from core.relationships import CollaborativeStrategyPriority


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
        return ", ".join([priority.ncff_team.ncff_team_name for priority in obj.ncffteamstrategypriority_set.filter(is_priority=True)])

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


class StrategyPriorityAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'community_collab')
    search_fields = ('strategy', 'community_collab')
