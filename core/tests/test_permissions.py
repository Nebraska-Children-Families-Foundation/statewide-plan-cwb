"""
Tests for Community Action Step permissions according to CLAUDE.md requirements:

Community Collaborative Action Steps:
- Action Steps should be visible to logged in users only
- Only members of a Community Collaborative should be able to edit Action Steps related to that Community Collaborative
- Users with the role `Staff Member` or `NCFF Team Member` should be able to edit all Action Steps
- Action Steps should be associated with the Community Collaborative and the user who created it
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseForbidden

from core.plan_work.models import CommunityActionStep, Goal, Objective, Strategy
from core.plan_actors.models import CommunityCollaborative, NcffTeam, SystemPartner
from core.permissions import has_community_action_step_edit_permission
from users.models import AppUser


class CommunityActionStepPermissionTests(TestCase):
    """Test Community Action Step permissions according to CLAUDE.md requirements"""
    
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
        
        # Create System Partner
        self.system_partner = SystemPartner.objects.create(
            system_partner_name="Test System Partner",
            system_partner_short_name="TSP"
        )
        
        # Create users
        User = get_user_model()
        
        # Community Collaborative Users
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
        
        # NCFF Team User (Staff Member)
        self.ncff_user = User.objects.create_user(
            email='ncff@test.com',
            password='testpass123',
            first_name='NCFF',
            last_name='User',
            member_type=AppUser.MemberTypes.NCFF_TEAM,
            ncff_team=self.ncff_team
        )
        
        # System Partner User
        self.system_user = User.objects.create_user(
            email='system@test.com',
            password='testpass123',
            first_name='System',
            last_name='User',
            member_type=AppUser.MemberTypes.SYSTEM_PARTNER,
            system_partner=self.system_partner
        )
        
        # Superuser
        self.superuser = User.objects.create_superuser(
            email='admin@test.com',
            password='testpass123',
            first_name='Super',
            last_name='User'
        )
        
        # Create test action steps
        self.action_step1 = CommunityActionStep.objects.create(
            activity_name="Test Action Step 1",
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
        
        self.action_step2 = CommunityActionStep.objects.create(
            activity_name="Test Action Step 2", 
            activity_details="Test details 2",
            related_goal=self.goal,
            related_objective=self.objective,
            related_strategy=self.strategy,
            related_collaborative=self.collab2,
            community_creator=self.community_user2,
            activity_status="Not Started",
            completedby_year=2024,
            completedby_quarter="Q2"
        )
        
        self.client = Client()

    def test_community_user_can_edit_own_action_step(self):
        """Test: Community user can edit action steps they created"""
        can_edit = has_community_action_step_edit_permission(
            self.community_user1, self.action_step1
        )
        self.assertTrue(can_edit, "Community user should be able to edit their own action step")

    def test_community_user_can_edit_collaborative_action_step(self):
        """Test: Community user can edit action steps from their collaborative"""
        # Create another user in the same collaborative
        User = get_user_model()
        another_user = User.objects.create_user(
            email='another@test.com',
            password='testpass123',
            member_type=AppUser.MemberTypes.COMMUNITY_COLLABORATIVE,
            community_collaborative=self.collab1
        )
        
        can_edit = has_community_action_step_edit_permission(
            another_user, self.action_step1
        )
        self.assertTrue(can_edit, "Community user should be able to edit action steps from their collaborative")

    def test_community_user_cannot_edit_other_collaborative_action_step(self):
        """Test: Community user cannot edit action steps from other collaboratives"""
        can_edit = has_community_action_step_edit_permission(
            self.community_user1, self.action_step2
        )
        self.assertFalse(can_edit, "Community user should not be able to edit action steps from other collaboratives")

    def test_ncff_user_can_edit_all_action_steps(self):
        """Test: NCFF Team Members can edit all Community Action Steps"""
        can_edit1 = has_community_action_step_edit_permission(
            self.ncff_user, self.action_step1
        )
        can_edit2 = has_community_action_step_edit_permission(
            self.ncff_user, self.action_step2
        )
        self.assertTrue(can_edit1, "NCFF Team Member should be able to edit all action steps")
        self.assertTrue(can_edit2, "NCFF Team Member should be able to edit all action steps")

    def test_superuser_can_edit_all_action_steps(self):
        """Test: Superuser can edit all Community Action Steps"""
        can_edit1 = has_community_action_step_edit_permission(
            self.superuser, self.action_step1
        )
        can_edit2 = has_community_action_step_edit_permission(
            self.superuser, self.action_step2
        )
        self.assertTrue(can_edit1, "Superuser should be able to edit all action steps")
        self.assertTrue(can_edit2, "Superuser should be able to edit all action steps")

    def test_system_partner_cannot_edit_community_action_steps(self):
        """Test: System Partner users cannot edit Community Action Steps"""
        can_edit1 = has_community_action_step_edit_permission(
            self.system_user, self.action_step1
        )
        can_edit2 = has_community_action_step_edit_permission(
            self.system_user, self.action_step2
        )
        self.assertFalse(can_edit1, "System Partner should not be able to edit community action steps")
        self.assertFalse(can_edit2, "System Partner should not be able to edit community action steps")

    def test_action_step_associated_with_creator_and_collaborative(self):
        """Test: Action Steps are associated with both creator and collaborative"""
        self.assertEqual(
            self.action_step1.community_creator, 
            self.community_user1,
            "Action step should be associated with its creator"
        )
        self.assertEqual(
            self.action_step1.related_collaborative,
            self.collab1,
            "Action step should be associated with the creator's collaborative"
        )

    def test_anonymous_user_cannot_access_edit_view(self):
        """Test: Non-logged in users cannot access edit views"""
        response = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step1.activity_id})
        )
        # Should redirect to login or return 403
        self.assertIn(response.status_code, [302, 403], 
                     "Anonymous users should not be able to access edit views")

    def test_logged_in_user_without_permission_gets_403(self):
        """Test: Logged in users without permission get 403 Forbidden"""
        # Log in as community_user1 but try to edit action_step2 (different collaborative)
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step2.activity_id})
        )
        self.assertEqual(response.status_code, 403, 
                        "Users without permission should get 403 Forbidden")

    def test_authorized_user_can_access_edit_view(self):
        """Test: Authorized users can access edit views"""
        # Log in as community_user1 and try to edit action_step1 (their own)
        self.client.login(email='community1@test.com', password='testpass123')
        response = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step1.activity_id})
        )
        self.assertEqual(response.status_code, 200, 
                        "Authorized users should be able to access edit views")

    def test_ncff_user_can_access_all_edit_views(self):
        """Test: NCFF Team Members can access all edit views"""
        self.client.login(email='ncff@test.com', password='testpass123')
        
        response1 = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step1.activity_id})
        )
        response2 = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step2.activity_id})
        )
        
        self.assertEqual(response1.status_code, 200, 
                        "NCFF Team Member should be able to access all edit views")
        self.assertEqual(response2.status_code, 200, 
                        "NCFF Team Member should be able to access all edit views")

    def test_superuser_can_access_all_edit_views(self):
        """Test: Superuser can access all edit views"""
        self.client.login(email='admin@test.com', password='testpass123')
        
        response1 = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step1.activity_id})
        )
        response2 = self.client.get(
            reverse('edit_community_activity', kwargs={'activity_id': self.action_step2.activity_id})
        )
        
        self.assertEqual(response1.status_code, 200, 
                        "Superuser should be able to access all edit views")
        self.assertEqual(response2.status_code, 200, 
                        "Superuser should be able to access all edit views")