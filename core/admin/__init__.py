from django.contrib import admin

from .alignment_admin import PerformanceMeasureAdmin, ChangeIndicatorAdmin
from .planwork_admin import StrategyAdmin, ObjectiveAdmin, GoalAdmin
from .planactors_admin import (CommunityCollaborativeAdmin, NcffTeamStrategyPriorityInline,
                               CollaborativeStrategyPriorityInline, PartnerStrategyPriorityInline, SystemPartnerAdmin,
                               NcffTeamAdmin)
from .standardization_admin import ActivityStatusAdmin
from .actionsteps_admin import SystemPartnerCommitmentAdmin, CommunityActionStepAdmin, NCActionStepAdmin
from ..measurement.models import PerformanceMeasure, ChangeIndicator
from ..plan_actors.models import NcffTeam, SystemPartner, CommunityCollaborative
from ..plan_work.models import Strategy, Objective, Goal, SystemPartnerCommitment, CommunityActionStep, NCActionStep
from ..standardization.models import ActivityStatus

admin.site.register(PerformanceMeasure, PerformanceMeasureAdmin)
admin.site.register(ChangeIndicator, ChangeIndicatorAdmin)
admin.site.register(NcffTeam, NcffTeamAdmin)
admin.site.register(SystemPartner, SystemPartnerAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(Objective, ObjectiveAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(SystemPartnerCommitment, SystemPartnerCommitmentAdmin)
admin.site.register(CommunityActionStep, CommunityActionStepAdmin)
admin.site.register(NCActionStep, NCActionStepAdmin)
admin.site.register(CommunityCollaborative, CommunityCollaborativeAdmin)