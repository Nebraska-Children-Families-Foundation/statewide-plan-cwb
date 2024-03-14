import uuid
from django.db import models


class NcffTeam(models.Model):
    ncff_team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ncff_team_name = models.CharField(max_length=50)
    ncff_team_short_name = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.ncff_team_short_name or self.ncff_team_name

    class Meta:
        verbose_name = 'NCFF Initiative / Team / Priority Area'
        verbose_name_plural = 'NCFF Initiatives / Teams / Priority Areas'
        db_table = 'ncff_team'
        ordering = ('ncff_team_name',)


class SystemPartner(models.Model):
    system_partner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_partner_name = models.CharField(max_length=75)
    system_partner_short_name = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.system_partner_short_name or self.system_partner_name

    class Meta:
        verbose_name = 'System Partner to Align & Support'
        verbose_name_plural = 'System Partners to Align & Support'
        db_table = 'system_partners'
        ordering = ('system_partner_name',)


class CommunityCollaborative(models.Model):
    community_collab_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community_collab_name = models.CharField(max_length=100)
    community_collab_short_name = models.CharField(max_length=25, unique=True, blank=True, null=True)

    def __str__(self):
        return self.community_collab_name or self.community_collab_name

    class Meta:
        verbose_name = 'Community Collaborative'
        verbose_name_plural = 'Community Collaboratives'
        db_table = 'community_collab'
        ordering = ('community_collab_name',)