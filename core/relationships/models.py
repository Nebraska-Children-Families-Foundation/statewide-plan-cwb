import uuid
from django.db import models


class StrategyPriority(models.Model):
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
        ordering = ['community_collaborative', 'strategy',]
