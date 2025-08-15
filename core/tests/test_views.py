"""
Tests for Community Action Step views and edit functionality
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages

from core.plan_work.models import CommunityActionStep, Goal, Objective, Strategy
from core.plan_actors.models import CommunityCollaborative, NcffTeam
from users.models import AppUser


class CommunityActionStepViewTests(TestCase):
    """Test Community Action Step views and functionality"""
    
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
        
        # Create Community Collaboratives
        self.collab1 = CommunityCollaborative.objects.create(
            community_collab_name="Test Collaborative 1",
            community_collab_short_name="TC1"
        )
        self.collab2 = CommunityCollaborative.objects.create(
            community_collab_name="Test Collaborative 2",
            community_collab_short_name="TC2"
        )
        
        # Create NCFF Team
        self.ncff_team = NcffTeam.objects.create(
            ncff_team_name="Test NCFF Team",
            ncff_team_short_name="TNT"
        )
        
        # Create users
        User = get_user_model()
        
        self.community_user1 = User.objects.create_user(
            email='community1@test.com',
            password='testpass123',
            first_name='Community',
            last_name='User1',
            member_type=AppUser.MemberTypes.COMMUNITY_COLLABORATIVE,
            community_collaborative=self.collab1
        )
        
        self.community_user2 = User.objects.create_user(
            email='community2@test.com',
            password='testpass123',
            first_name='Community',
            last_name='User2',
            member_type=AppUser.MemberTypes.COMMUNITY_COLLABORATIVE,
            community_collaborative=self.collab2
        )
        
        self.ncff_user = User.objects.create_user(
            email='ncff@test.com',
            password='testpass123',
            first_name='NCFF',
            last_name='User',
            member_type=AppUser.MemberTypes.NCFF_TEAM,
            ncff_team=self.ncff_team
        )
        
        # Create test action step
        self.action_step = CommunityActionStep.objects.create(
            activity_name="Test Action Step",
            activity_details="Test details",
            related_goal=self.goal,
            related_objective=self.objective,
            related_strategy=self.strategy,
            related_collaborative=self.collab1,
            community_creator=self.community_user1,
            activity_status="Not Started",
            completedby_year=2024,
            completedby_quarter="Q1"
        )
        
        self.client = Client()

    def test_edit_view_displays_form_with_correct_data(self):
        """Test: Edit view displays form with current action step data"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step.activity_id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.action_step.activity_name)
        self.assertContains(response, self.action_step.activity_details)
        self.assertContains(response, 'Edit Community Action Step')

    def test_edit_form_submission_updates_action_step(self):
        """Test: Submitting edit form updates the action step"""
        self.client.login(email='community1@test.com', password='testpass123')
        
        updated_data = {
            'activity_name': 'Updated Action Step Name',
            'activity_details': 'Updated details',
            'activity_lead': 'Updated Lead',
            'activity_status': 'In Progress',
            'completedby_year': 2025,
            'completedby_quarter': 'Q2',
            'related_goal': self.goal.pk,
            'related_objective': self.objective.pk,
            'related_strategy': self.strategy.pk,
            'related_collaborative': self.collab1.pk
        }
        
        response = self.client.post(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step.activity_id}),
            data=updated_data
        )
        
        # Should redirect after successful update
        self.assertEqual(response.status_code, 302)
        
        # Check that the action step was updated
        self.action_step.refresh_from_db()
        self.assertEqual(self.action_step.activity_name, 'Updated Action Step Name')
        self.assertEqual(self.action_step.activity_details, 'Updated details')
        self.assertEqual(self.action_step.activity_status, 'In Progress')

    def test_edit_form_shows_success_message(self):
        """Test: Edit form shows success message after update"""
        self.client.login(email='community1@test.com', password='testpass123')
        
        updated_data = {
            'activity_name': 'Updated Action Step Name',
            'activity_details': 'Updated details',
            'activity_lead': 'Updated Lead',
            'activity_status': 'In Progress',
            'completedby_year': 2025,
            'completedby_quarter': 'Q2',
            'related_goal': self.goal.pk,
            'related_objective': self.objective.pk,
            'related_strategy': self.strategy.pk,
            'related_collaborative': self.collab1.pk
        }
        
        response = self.client.post(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step.activity_id}),
            data=updated_data,
            follow=True
        )
        
        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('updated successfully' in str(m) for m in messages))

    def test_edit_view_shows_readonly_plan_alignment(self):
        """Test: Edit view shows plan alignment as read-only"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step.activity_id})
        )
        
        self.assertContains(response, 'Plan Alignment (Read Only)')
        self.assertContains(response, str(self.action_step.related_goal))
        self.assertContains(response, str(self.action_step.related_objective))
        self.assertContains(response, str(self.action_step.related_strategy))

    def test_my_activities_view_shows_edit_buttons_for_authorized_users(self):
        """Test: My activities view shows edit buttons for authorized users"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(reverse('list_my_community_activities'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit')
        self.assertContains(response, reverse('edit_community_activity', 
                                            kwargs={'activity_id': self.action_step.activity_id}))

    def test_my_activities_view_shows_delete_button_for_creators(self):
        """Test: My activities view shows delete button for action step creators"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(reverse('list_my_community_activities'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delete')
        self.assertContains(response, reverse('delete_community_activity', 
                                            kwargs={'activity_id': self.action_step.activity_id}))

    def test_activity_details_shows_edit_button_for_authorized_users(self):
        """Test: Activity details shows edit button for authorized users"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(
            reverse('activity_details', kwargs={'activity_id': self.action_step.activity_id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Action Step')
        self.assertContains(response, reverse('edit_community_activity', 
                                            kwargs={'activity_id': self.action_step.activity_id}))

    def test_activity_details_hides_edit_button_for_unauthorized_users(self):
        """Test: Activity details hides edit button for unauthorized users"""
        self.client.login(email='community2@test.com', password='testpass123')
        response = self.client.get(
            reverse('activity_details', kwargs={'activity_id': self.action_step.activity_id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit Action Step')

    def test_ncff_user_sees_edit_buttons_for_all_action_steps(self):
        """Test: NCFF users see edit buttons for all action steps"""
        self.client.login(email='ncff@test.com', password='testpass123')
        
        # Test activity details
        response = self.client.get(
            reverse('activity_details', kwargs={'activity_id': self.action_step.activity_id})
        )
        self.assertContains(response, 'Edit Action Step')
        
        # Test dashboard
        response = self.client.get(reverse('individual_dashboard'))
        # NCFF user should see edit buttons in dashboard if they have any action steps

    def test_dashboard_shows_edit_buttons_in_actions_column(self):
        """Test: Dashboard shows edit buttons in actions column"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(reverse('individual_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        # Should contain edit icon and link
        self.assertContains(response, 'bi-pencil')
        self.assertContains(response, reverse('edit_community_activity', 
                                            kwargs={'activity_id': self.action_step.activity_id}))

    def test_community_activities_list_shows_edit_buttons(self):
        """Test: Community activities list shows edit buttons for authorized users"""
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(
            reverse('community_activities', kwargs={'strategy_id': self.strategy.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Action Step')
        self.assertContains(response, reverse('edit_community_activity', 
                                            kwargs={'activity_id': self.action_step.activity_id}))