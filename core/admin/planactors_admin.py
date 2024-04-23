from django.contrib import admin

from core.models import CommunityActionStep
from core.relationships import CollaborativeStrategyPriority
from core.relationships.models import NcffTeamStrategyPriority, PartnerStrategyPriority


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


class SystemPartnerAdmin(admin.ModelAdmin):
    list_display = ('system_partner_name', 'system_partner_short_name', 'strategy_count',)
    search_fields = ('system_partner_name', 'system_partner_short_name',)
    ordering = ('system_partner_name',)

    def strategy_count(self, obj):  # Counts number of Strategies assigned to the partner.
        return obj.strategy_set.count()
    strategy_count.short_description = '# of Strategies Assigned'


class NcffTeamAdmin(admin.ModelAdmin):
    list_display = ('ncff_team_name', 'strategy_count')
    search_fields = ('ncff_team_name',)

    def strategy_count(self, obj):  # Counts number of Strategies assigned to the team.
        return obj.strategy_set.count()
    strategy_count.short_description = '# of Strategies Assigned'
