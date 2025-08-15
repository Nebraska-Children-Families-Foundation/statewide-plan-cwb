"""
Tests for Action Step visibility according to CLAUDE.md requirements:

- Action Steps should be visible to logged in users only
- Non-logged in users should not be able to see Action Step information
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.plan_work.models import CommunityActionStep, Goal, Objective, Strategy
from core.plan_actors.models import CommunityCollaborative
from users.models import AppUser


class ActionStepVisibilityTests(TestCase):
    """Test Action Step visibility for logged in vs anonymous users"""
    
    def setUp(self):
        """Set up test data"""
        # Create test Goal, Objective, Strategy
        self.goal = Goal.objects.create(
            goal_number=1,
            goal_name="Test Goal"
        )
        self.objective = Objective.objects.create(
            objective_number=1,
            objective_name="Test Objective",
            related_goal=self.goal
        )
        self.strategy = Strategy.objects.create(
            strategy_number="STRG-0001",
            strategy_name="Test Strategy",
            related_objective=self.objective,
            related_goal=self.goal
        )
        
        # Create Community Collaborative
        self.collab = CommunityCollaborative.objects.create(
            community_collab_name="Test Collaborative",
            community_collab_short_name="TC"
        )
        
        # Create user
        User = get_user_model()
        self.community_user = User.objects.create_user(
            email='community@test.com',
            password='testpass123',
            first_name='Community',
            last_name='User',
            member_type=AppUser.MemberTypes.COMMUNITY_COLLABORATIVE,
            community_collaborative=self.collab
        )
        
        # Create test action step
        self.action_step = CommunityActionStep.objects.create(
            activity_name="Test Action Step",
            activity_details="Test details",
            related_goal=self.goal,
            related_objective=self.objective,
            related_strategy=self.strategy,
            related_collaborative=self.collab,
            community_creator=self.community_user,
            activity_status="Not Started",
            completedby_year=2024,
            completedby_quarter="Q1"
        )
        
        self.client = Client()

    def test_anonymous_user_cannot_access_activity_details(self):
        """Test: Anonymous users cannot access activity details"""
        response = self.client.get(
            reverse('activity_details', kwargs={'activity_id': self.action_step.activity_id})
        )
        # Should redirect to login or return 403/404
        self.assertIn(response.status_code, [302, 403, 404], 
                     "Anonymous users should not be able to access activity details")

    def test_anonymous_user_cannot_access_community_activities_list(self):
        """Test: Anonymous users cannot access community activities list"""
        response = self.client.get(
            reverse('community_activities', kwargs={'strategy_id': self.strategy.pk})
        )
        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403], 
                     "Anonymous users should not be able to access community activities list")

    def test_anonymous_user_cannot_access_my_activities(self):
        """Test: Anonymous users cannot access my activities page"""
        response = self.client.get(reverse('list_my_community_activities'))
        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403], 
                     "Anonymous users should not be able to access my activities page")

    def test_anonymous_user_cannot_access_dashboard(self):
        """Test: Anonymous users cannot access individual dashboard"""
        response = self.client.get(reverse('individual_dashboard'))
        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403], 
                     "Anonymous users should not be able to access dashboard")

    def test_logged_in_user_can_access_activity_details(self):
        """Test: Logged in users can access activity details"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(
            reverse('activity_details', kwargs={'activity_id': self.action_step.activity_id})
        )
        self.assertEqual(response.status_code, 200, 
                        "Logged in users should be able to access activity details")

    def test_logged_in_user_can_access_community_activities_list(self):
        """Test: Logged in users can access community activities list"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(
            reverse('community_activities', kwargs={'strategy_id': self.strategy.pk})
        )
        self.assertEqual(response.status_code, 200, 
                        "Logged in users should be able to access community activities list")

    def test_logged_in_user_can_access_my_activities(self):
        """Test: Logged in users can access my activities page"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(reverse('list_my_community_activities'))
        self.assertEqual(response.status_code, 200, 
                        "Logged in users should be able to access my activities page")

    def test_logged_in_user_can_access_dashboard(self):
        """Test: Logged in users can access individual dashboard"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(reverse('individual_dashboard'))
        self.assertEqual(response.status_code, 200, 
                        "Logged in users should be able to access dashboard")

    def test_activity_details_contain_action_step_info(self):
        """Test: Activity details contain action step information for logged in users"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(
            reverse('activity_details', kwargs={'activity_id': self.action_step.activity_id})
        )
        
        self.assertContains(response, self.action_step.activity_name, 
                           msg_prefix="Activity details should contain action step name")
        self.assertContains(response, self.action_step.activity_details, 
                           msg_prefix="Activity details should contain action step details")

    def test_community_activities_list_shows_action_steps(self):
        """Test: Community activities list shows action steps for logged in users"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(
            reverse('community_activities', kwargs={'strategy_id': self.strategy.pk})
        )
        
        self.assertContains(response, self.action_step.activity_name, 
                           msg_prefix="Community activities list should contain action step name")
        self.assertContains(response, self.action_step.activity_number, 
                           msg_prefix="Community activities list should contain action step number")

    def test_my_activities_shows_user_action_steps(self):
        """Test: My activities page shows user's action steps"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(reverse('list_my_community_activities'))
        
        self.assertContains(response, self.action_step.activity_name, 
                           msg_prefix="My activities should contain user's action step name")
        self.assertContains(response, self.action_step.activity_number, 
                           msg_prefix="My activities should contain user's action step number")

    def test_dashboard_shows_user_action_steps(self):
        """Test: Dashboard shows user's action steps"""
        self.client.login(email='community@test.com', password='testpass123')
        response = self.client.get(reverse('individual_dashboard'))
        
        self.assertContains(response, self.action_step.activity_name, 
                           msg_prefix="Dashboard should contain user's action step name")
        self.assertContains(response, self.action_step.activity_number, 
                           msg_prefix="Dashboard should contain user's action step number")