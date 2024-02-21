import uuid
from django.db import models
from smart_selects.db_fields import ChainedForeignKey


# Enums
class ActivityStatusChoice(models.TextChoices):
    NOT_STARTED = 'Not Started', 'Not Started'
    IN_PROGRESS = 'In Progress', 'In Progress'
    COMPLETED = 'Completed', 'Completed'
    ONGOING = 'Ongoing', 'Ongoing'


class Quarters(models.TextChoices):
    Q1 = 'Q1', 'Q1'
    Q2 = 'Q2', 'Q2'
    Q3 = 'Q3', 'Q3'
    Q4 = 'Q4', 'Q4'


class Years(models.TextChoices):
    Y2022 = '2022', '2022'
    Y2023 = '2023', '2023'
    Y2024 = '2024', '2024'
    Y2025 = '2025', '2025'
    Y2026 = '2026', '2026'
    Y2027 = '2027', '2027'


# cwb_choice models
class ActivityStatus(models.Model):
    activity_status_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_status = models.CharField(max_length=25)

    def __str__(self):
        return self.activity_status


class NcffTeam(models.Model):
    ncff_team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ncff_team_name = models.CharField(max_length=50)

    def __str__(self):
        return self.ncff_team_name


class CommunityCollaborative(models.Model):
    community_collab_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community_collab_name = models.CharField(max_length=100)
    community_collab_short_name = models.CharField(max_length=25)

    def __str__(self):
        return self.community_collab_name


# cwb_supp models
class ChangeIndicator(models.Model):
    indicator_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    indicator = models.CharField(max_length=255)

    def __str__(self):
        return self.indicator


class PerformanceMeasure(models.Model):
    measure_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    measure = models.CharField(max_length=255)

    def __str__(self):
        return self.measure


class DhhsPriority(models.Model):
    dhhs_priority_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    priority_description = models.CharField(max_length=255)

    def __str__(self):
        return self.priority_description


# cwb_core models

class Goal(models.Model):
    goal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal_number = models.IntegerField()
    goal_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.goal_number)


class Objective(models.Model):
    objective_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objective_number = models.IntegerField()
    objective_name = models.CharField(max_length=255)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)

    def __str__(self):
        return f"Goal {self.related_goal.goal_number}, Objective {self.objective_number}"


class Strategy(models.Model):
    strategy_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    strategy_number = models.CharField(max_length=9)
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

    def __str__(self):
        return (f"Goal {self.related_goal.goal_number}, Obj {self.related_objective.objective_number}, "
                f"Strategy {self.strategy_number}")


class CommunityActivity(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_number = models.CharField(max_length=10)
    activity_name = models.CharField(max_length=255)
    activity_details = models.TextField(max_length=500)
    activity_lead = models.CharField(max_length=100)
    activity_status = models.CharField(max_length=25, choices=ActivityStatusChoice.choices)
    completedby_year = models.CharField(max_length=4, choices=Years.choices)
    completedby_quarter = models.CharField(max_length=2, choices=Quarters.choices)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    related_collaborative = models.ForeignKey(CommunityCollaborative, on_delete=models.CASCADE)
    related_strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    related_objective = models.ForeignKey('Objective', on_delete=models.CASCADE)

    def __str__(self):
        return (f"[{self.related_collaborative.community_collab_short_name}] - Goal {self.related_goal}, "
                f"Objective {self.related_objective}, Strategy {self.related_strategy}")



class StrategyActivity(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_number = models.CharField(max_length=10)
    activity_name = models.CharField(max_length=255)
    activity_details = models.TextField(max_length=500)
    activity_lead = models.CharField(max_length=100)
    activity_priority = models.BooleanField()
    activity_status = models.CharField(max_length=25, choices=ActivityStatusChoice.choices)
    completedby_year = models.CharField(max_length=4, choices=Years.choices)
    completedby_quarter = models.CharField(max_length=2, choices=Quarters.choices)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    related_strategy = models.ForeignKey('Strategy', on_delete=models.CASCADE)
    related_objective = models.ForeignKey('Objective', on_delete=models.CASCADE)

    def __str__(self):
        return (f"Goal {self.related_goal.goal_number}, Obj. {self.related_objective.objective_number}, "
                f"Strategy {self.related_strategy.strategy_number}")


# cwb_junction model
class StrategyPriority(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    community_collab = models.ForeignKey(CommunityCollaborative, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('strategy', 'community_collab')
