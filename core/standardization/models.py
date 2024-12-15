# core/standardization/models.py
"""
The Standardization module provides standard terms that are used in dropdowns and filtering across the plan.
"""

import uuid
from django.db import models


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
    NotApplicable = 'N/A', 'N/A'


class Years(models.TextChoices):
    Y2022 = '2022', '2022'
    Y2023 = '2023', '2023'
    Y2024 = '2024', '2024'
    Y2025 = '2025', '2025'
    Y2026 = '2026', '2026'
    Y2027 = '2027', '2027'
    NotApplicable = 'N/A', 'N/A'


# cwb_choice models
class ActivityStatus(models.Model):
    activity_status_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_status = models.CharField(max_length=25)

    def __str__(self):
        return self.activity_status

    class Meta:
        verbose_name = 'Activity Status'
        verbose_name_plural = 'Activity Statuses'
        db_table = 'activity_statuses'
        ordering = ('activity_status',)
