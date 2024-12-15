from django.urls import path, include
from . import views
from rest_framework import routers
from .views import ActionStepsViewSet

router = routers.DefaultRouter()
router.register(r'api/action-steps', ActionStepsViewSet, basename='action-steps')

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('communication-plan/', views.communication_plan, name='communication_plan'),
    path('goals/', views.goals, name='goals'),
    path('strategies-objectives/', views.strategies_objectives, name='strategies_objectives'),
    path('community-activities/<uuid:strategy_id>/', views.community_activities, name='community_activities'),
    path('partner-activities/<uuid:strategy_id>/', views.partner_activities, name='partner_activities'),
    path('community-collaboratives/', views.community_collaboratives, name='community_collaboratives'),
    path('activities', views.activities, name='activities'),
    path('create-strategy', views.create_strategy, name='create_strategy'),
    path('strategies/<uuid:objective_id>/', views.strategies, name='strategies'),
    path('strategy-list/', views.strategy_list, name='strategy_list'),
    path('ajax/load-objectives/', views.load_objectives, name='ajax_load_objectives'),
    path('community-activities/<uuid:strategy_id>/', views.community_activities, name='community_activities'),
    path('partner-activities/<uuid:strategy_id>/', views.partner_activities, name='partner_activities'),
    path('nc-activities/<uuid:strategy_id>/', views.nc_activities, name='nc_activities'),
    path('create-community-activity/', views.create_community_activity, name='create_community_activity'),
    path('create-partner-activity/', views.create_partner_commitment, name='create_partner_activity'),
    path('create-nc-action-step/', views.create_nc_activity, name='create_nc_activity'),
    path('it-worked/', views.it_worked, name='it_worked'),
    path('reports/', views.reports, name='reports'),
    path('privacy', views.privacy, name='privacy'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
    path('dashboard/', views.individual_dashboard, name='individual_dashboard'),
    path('activity/<uuid:activity_id>/', views.activity_details, name='activity_details'),
    # Action Steps URLs
    path('action-steps/', views.action_steps_view, name='action_steps'),
    path('api/action-steps/actors/', views.get_actors, name='get_actors'),
    path('api/action-steps/data/', views.get_action_steps_data, name='get_action_steps_data'),
    path('api/action-steps/objectives/<uuid:goal_id>/', views.get_objectives, name='get_objectives'),
    path('api/action-steps/strategies/<uuid:objective_id>/', views.get_strategies, name='get_strategies'),
    path('', include(router.urls)),
]
