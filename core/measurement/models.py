import uuid
from django.db import models


class ChangeIndicator(models.Model):
    indicator_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    indicator = models.CharField(max_length=255)

    def __str__(self):
        return self.indicator

    class Meta:
        verbose_name = 'Indicator of Change'
        verbose_name_plural = 'Indicators of Change'
        db_table = 'change_indicator'
        ordering = ('indicator',)


class PerformanceMeasure(models.Model):
    measure_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    measure = models.CharField(max_length=255)

    def __str__(self):
        return self.measure

    class Meta:
        verbose_name = 'Performance Measure'
        verbose_name_plural = 'Performance Measures'
        db_table = 'performance_measure'
        ordering = ('measure',)
