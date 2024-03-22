import uuid
from django.db import models


class CollaborativeStrategyPriority(models.Model):
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    community_collaborative = models.ForeignKey('CommunityCollaborative', on_delete=models.CASCADE)
    is_priority = models.BooleanField(default=False)

    def __str__(self):
        collaborative_str = str(
            self.community_collaborative) if self.community_collaborative else "Unknown Collaborative"
        strategy_str = str(self.strategy) if self.strategy else "Unknown Strategy"
        return f"{collaborative_str} - {strategy_str} - Priority: {self.is_priority}"

    class Meta:
        unique_together = ('strategy', 'community_collaborative')
        verbose_name = 'Community Collab Priority'
        verbose_name_plural = 'Community Collab Priorities'
        db_table = 'collab_strategy_priority'
        ordering = ['community_collaborative', 'strategy', ]


class NcffTeamStrategyPriority(models.Model):
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    ncff_team = models.ForeignKey('NcffTeam', on_delete=models.CASCADE)
    is_priority = models.BooleanField(default=False)

    def __str__(self):
        team_str = str(self.ncff_team.ncff_team_name) if self.ncff_team else "Unknown Team"
        strategy_str = str(self.strategy.strategy_name) if self.strategy else "Unknown Strategy"
        return f"{team_str} - {strategy_str} - Priority: {self.is_priority}"

    class Meta:
        unique_together = ('strategy', 'ncff_team')
        verbose_name = 'NCFF Team Priority'
        verbose_name_plural = 'NCFF Team Priorities'
        db_table = 'ncff_strategy_priority'
        ordering = ['ncff_team', 'strategy', ]


class PartnerStrategyPriority(models.Model):
    strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    system_partner = models.ForeignKey('SystemPartner', on_delete=models.CASCADE)
    is_priority = models.BooleanField(default=False)

    def __str__(self):
        partner_str = str(self.system_partner.system_partner_name) if self.system_partner else "Unknown Partner"
        strategy_str = str(self.strategy.strategy_name) if self.strategy else "Unknown Strategy"
        return f"{partner_str} - {strategy_str} - Priority: {self.is_priority}"

    class Meta:
        unique_together = ('strategy', 'system_partner')
        verbose_name = 'Partner Strategy Priority'
        verbose_name_plural = 'Partner Strategy Priorities'
        db_table = 'partner_strategy_priority'
        ordering = ['system_partner', 'strategy',]
