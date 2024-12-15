# core/plan_actors/models.py
"""
The Plan Actors module contains the entities that are tasked with accomplishing the Statewide Plan
for Community Well-Being. There are three main actors: the Community Collaboratives (e.g., Communities),
Nebraska Children and Families Foundation (e.g., Nebraska Children or NCFF), and System Partners
(generally government agencies, state/national foundations, or quasi-governmental organizations).

This module is designed to make it easy to update the names of System Partners, Community Collaboratives,
and teams at Nebraska Children. Additionally, this module makes it possible to filter the plan work by
those tasked with carrying it out.
"""

import uuid
from django.db import models


class NcffTeam(models.Model):
    ncff_team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ncff_team_name = models.CharField(max_length=50)
    ncff_team_short_name = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        # Use the short name if available; otherwise, use the full name.
        # Ensure that the result is always a string and provides a fallback default.
        return str(self.ncff_team_short_name or self.ncff_team_name or "Unnamed Team")

    class Meta:
        verbose_name = 'NCFF Initiative / Team / Priority Area'
        verbose_name_plural = 'NCFF Initiatives / Teams / Priority Areas'
        db_table = 'ncff_team'
        ordering = ('ncff_team_name',)


class SystemPartner(models.Model):
    system_partner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_partner_name = models.CharField(max_length=75)
    system_partner_short_name = models.CharField(max_length=25, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = None

    def __str__(self):
        # Use the short name if available; otherwise, use the full name.
        # Ensure that the result is always a string and provides a fallback default.
        return self.system_partner_short_name or self.system_partner_name or "Unnamed Partner"

    class Meta:
        verbose_name = 'System Partner to Align & Support'
        verbose_name_plural = 'System Partners to Align & Support'
        db_table = 'system_partners'
        ordering = ('system_partner_name',)


class CommunityCollaborative(models.Model):
    community_collab_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community_collab_short_name = models.CharField(max_length=25, blank=True, null=True)
    community_collab_name = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = None

    def __str__(self):
        # Use the short name if available; otherwise, use the full name.
        # Ensure that the result is always a string and provides a fallback default.
        return self.community_collab_short_name or self.community_collab_name or "Unnamed Collaborative"

    class Meta:
        verbose_name = 'Community Collaborative'
        verbose_name_plural = 'Community Collaboratives'
        db_table = 'community_collab'
        ordering = ('community_collab_name',)
