import uuid
from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from core.standardization import ActivityStatusChoice, Quarters, Years
from core.plan_actors import CommunityCollaborative


class Goal(models.Model):
    goal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal_number = models.IntegerField()
    goal_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.goal_number) or str(self.goal_name)

    class Meta:
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'
        db_table = 'goal'
        ordering = ('goal_number',)


class Objective(models.Model):
    objective_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objective_number = models.IntegerField()
    objective_name = models.CharField(max_length=255)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)

    def __str__(self):
        return (f"Goal {self.related_goal.goal_number}, Objective {self.objective_number}" or
                f"Objective {self.objective_number}: {self.objective_name}")

    class Meta:
        verbose_name = 'Objective'
        verbose_name_plural = 'Objectives'
        db_table = 'objective'
        ordering = ('related_goal', 'objective_number',)


class Strategy(models.Model):
    strategy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strategy_number = models.CharField(max_length=9, help_text="Automatically generated. No need to set manually.")
    strategy_name = models.CharField(max_length=255)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    related_objective = ChainedForeignKey(
        Objective,
        chained_field="related_goal",  # The field in this model to chain from.
        chained_model_field="related_goal",  # The field in Objective model that relates to Goal.
        show_all=False,
        auto_choose=True,
        sort=True,
    )

    # Functionality that increments the strategy number is the STRG-XXXX format.
    def save(self, *args, **kwargs):
        if not self.strategy_number:
            prefix = "STRG-"
            last_strategy = Strategy.objects.order_by('strategy_number').last()

            if last_strategy:
                last_number = int(last_strategy.strategy_number.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1000  # Start from 1000

            self.strategy_number = f"{prefix}{new_number}"
        super().save(*args, **kwargs)

    ncff_teams = models.ManyToManyField('NcffTeam', blank=True)
    system_partners = models.ManyToManyField('SystemPartner', blank=True)

    community_collaboratives = models.ManyToManyField(
        'CommunityCollaborative',
        through='StrategyPriority',
        blank=True
    )

    def __str__(self):
        return (f"Goal {self.related_goal.goal_number}, Obj {self.related_objective.objective_number}, "
                f"Strategy {self.strategy_number}")

    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategies'
        db_table = 'strategy'
        ordering = ('related_goal', 'related_objective', 'strategy_number',)


class CommunityActivity(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_number = models.CharField(max_length=10, help_text="Automatically generated. No need to set manually.")
    activity_name = models.CharField(max_length=255)
    activity_details = models.TextField(max_length=1200)
    activity_lead = models.CharField(max_length=100,
                                     help_text="Indicate who will lead to the activity (person or organization).",
                                     blank=True, default="")
    activity_status = models.CharField(max_length=25, choices=ActivityStatusChoice.choices)
    completedby_year = models.CharField(max_length=4, choices=Years.choices, blank=True)
    completedby_quarter = models.CharField(max_length=3, choices=Quarters.choices, blank=True)
    related_collaborative = models.ForeignKey(CommunityCollaborative, on_delete=models.CASCADE)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    related_objective = ChainedForeignKey(
        'Objective',
        chained_field="related_goal",
        chained_model_field="goal",
        show_all=False,
        auto_choose=True,
        sort=True)
    related_strategy = ChainedForeignKey(
        'Strategy',
        chained_field="related_objective",
        chained_model_field="objective",
        show_all=False,
        auto_choose=True,
        sort=True)

    # Functionality that increments the strategy number is the C-ACT-1XXX format.
    def save(self, *args, **kwargs):
        if not self.activity_number:
            prefix = "C-ACT-"
            last_activity = CommunityActivity.objects.order_by('activity_number').last()

            if last_activity:
                # Splitting the string to extract the numeric part
                number_part = last_activity.activity_number.split('-')[2]
                last_number = int(number_part)  # Converting the extracted part to an integer
                new_number = last_number + 1
            else:
                new_number = 1000  # Start from 1000

            self.activity_number = f"{prefix}{new_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        collab_name = (self.related_collaborative.community_collab_short_name or
                       self.related_collaborative.community_collab_name)
        return (f"[{self.related_collaborative.community_collab_short_name}] - Goal {self.related_goal}, "
                f"Objective {self.related_objective}, Strategy {self.related_strategy}")

    class Meta:
        verbose_name_plural = 'Community Activity'
        verbose_name = 'Community Activities'
        db_table = 'community_activity'
        ordering = ['related_collaborative', 'related_goal', 'related_objective', 'related_strategy',
                    'activity_status', 'completedby_year',]


class StrategyActivity(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_number = models.CharField(max_length=10, help_text="Automatically generated. No need to set manually.")
    activity_name = models.CharField(max_length=255)
    activity_details = models.TextField(max_length=1500)
    activity_lead = models.CharField(max_length=100,
                                     help_text="Indicate who will lead the activity (person, organization, or team).",
                                     blank=True, default="")
    activity_priority = models.BooleanField()
    activity_status = models.CharField(max_length=25, choices=ActivityStatusChoice.choices)
    completedby_year = models.CharField(max_length=4, choices=Years.choices)
    completedby_quarter = models.CharField(max_length=3, choices=Quarters.choices)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    related_strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    related_objective = models.ForeignKey('Objective', on_delete=models.CASCADE)

    # Functionality that increments the strategy number is the ACT-1XXX format.
    def save(self, *args, **kwargs):
        if not self.activity_number:
            prefix = "ACT-"
            last_activity = StrategyActivity.objects.order_by('activity_number').last()

            if last_activity:
                last_number = int(last_activity.activity_number.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1000  # Start from 1000

            self.activity_number = f"{prefix}{new_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Goal {self.related_goal.goal_number}, Obj. {self.related_objective.objective_number}, "
                f"Strategy {self.related_strategy.strategy_number}")

    class Meta:
        verbose_name = "Strategy Activity"
        verbose_name_plural = "Strategy Activities"
        db_table = 'strategy_activity'
        ordering = ['related_goal', 'related_objective', 'related_strategy', 'activity_number', 'completedby_year',]
