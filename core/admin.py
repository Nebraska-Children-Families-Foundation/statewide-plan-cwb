from django.contrib import admin
from .models import (
    ActivityStatus, NcffTeam, CommunityCollaborative,
    ChangeIndicator, PerformanceMeasure, DhhsPriority,
    CommunityActivity, StrategyActivity, Strategy, Objective, Goal, SystemPartner, CollaborativeStrategyPriority
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
        return CommunityActivity.objects.filter(related_collaborative=obj).count()

    community_activity_count.short_description = 'Activity Count'


class StrategyPriorityInline(admin.TabularInline):
    # Specify the model that this inline admin will manage.
    model = CollaborativeStrategyPriority

    # Set the number of extra forms to display in the inline admin.
    # This allows for adding new StrategyPriority instances directly from the Strategy admin page.
    extra = 1

    # You can add more options here to customize the admin interface


class StrategyAdmin(admin.ModelAdmin):
    list_display = ('strategy_number', 'strategy_name', 'get_goal_number', 'get_goal_name', 'get_objective_number',
                    'get_objective_name', 'get_priority_collaboratives')
    search_fields = ('strategy_name', 'get_priority_collaboratives')
    list_filter = ('related_goal', 'related_objective', 'strategy_number',)
    ordering = ('strategy_number', 'related_goal', 'related_objective')
    inlines = [StrategyPriorityInline]

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
        return ", ".join([cc.community_collab_name for cc in
                          obj.community_collaboratives.filter(strategypriority__is_priority=True)])

    get_priority_collaboratives.short_description = 'Priority Collaboratives'

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
    list_display = ('activity_number', 'activity_name', 'activity_status', 'completedby_year', 'completedby_quarter')
    search_fields = ('activity_name', 'activity_status')

    readonly_fields = ('activity_number',)


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
