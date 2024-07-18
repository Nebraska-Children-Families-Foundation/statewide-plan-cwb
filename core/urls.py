from django.urls import path
from . import views
from .views import create_community_activity

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
    path('create-community-activity/', views.create_community_activity, name='create_community_activity'),
    path('create-partner-activity/', views.create_partner_commitment, name='create_partner_activity'),
    path('create-nc-action-step/', views.create_nc_activity, name='create_nc_activity'),
    path('it-worked/', views.it_worked, name='it_worked'),
    path('privacy', views.privacy, name='privacy'),
    path('terms-of-use', views.terms_of_use, name='terms_of_use'),
]
