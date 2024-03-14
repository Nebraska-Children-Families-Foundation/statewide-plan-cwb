import uuid
from django.db import models


class DhhsPriority(models.Model):
    dhhs_priority_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_goal = models.ForeignKey('Goal', on_delete=models.CASCADE)
    priority_description = models.CharField(max_length=255)

    def __str__(self):
        return self.priority_description

    class Meta:
        verbose_name = 'DHHS Priority'
        verbose_name_plural = 'DHHS Priorities'
        db_table = 'dhhs_priority'
        ordering = ('related_goal',)