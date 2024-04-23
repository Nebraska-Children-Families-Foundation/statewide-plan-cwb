from django.contrib import admin


class CommunityActionStepAdmin(admin.ModelAdmin):
    list_display = ('activity_number', 'activity_name', 'activity_status', 'completedby_year', 'completedby_quarter',
                    'related_collaborative')
    search_fields = ('activity_name', 'activity_status')
    list_filter = ('related_collaborative', 'activity_status')

    readonly_fields = ('activity_number',)

    def get_community_collab(self, obj):
        return obj.related_collaborative.community_collab_name

    get_community_collab.short_description = 'Community Collaborative'


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


class NCActionStepAdmin(admin.ModelAdmin):
    list_display = ('activity_number', 'activity_name', 'activity_status', 'completedby_year', 'completedby_quarter')
    search_fields = ('activity_name', 'activity_status')

    readonly_fields = ('activity_number',)
