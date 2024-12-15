from django import forms
from django.forms import ModelForm
from .models import (CommunityActionStep, NCActionStep, Goal, Objective, Strategy, SystemPartnerCommitment,
                     SystemPartner, NcffTeam, CommunityCollaborative, SystemPartner, ActivityStatusChoice,
                     Years, Quarters)
from django.db.models import F


class CommunityActivityForm(forms.ModelForm):
    class Meta:
        model = CommunityActionStep
        exclude = ['activity_number', 'community_creator']  # Exclude auto-managed fields
        widgets = {
            'activity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_details': forms.Textarea(attrs={'class': 'form-control'}),
            'activity_lead': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_status': forms.Select(attrs={'class': 'form-select'}),
            'completedby_year': forms.Select(attrs={'class': 'form-select'}),
            'completedby_quarter': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(CommunityActivityForm, self).__init__(*args, **kwargs)

        self.fields['related_goal'].label_from_instance = lambda obj: f"{obj.goal_number} - {obj.goal_name}"
        self.fields['related_objective'].label_from_instance = lambda obj: f"Obj {obj.objective_number} - {obj.objective_name}"
        self.fields['related_strategy'].label_from_instance = lambda obj: (f"{obj.related_goal.goal_number}, "
                                                                           f"Obj {obj.related_objective.objective_number} | "
                                                                           f"Strategy {obj.strategy_number} - {obj.strategy_name}")


class PartnerActivityForm(forms.ModelForm):
    class Meta:
        model = SystemPartnerCommitment
        exclude = ['commitment_number', 'system_partner_creator']  # Exclude these fields from the form
        widgets = {
            'commitment_name': forms.TextInput(attrs={'class': 'form-control'}),
            'commitment_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'commitment_lead': forms.TextInput(attrs={'class': 'form-control'}),
            'commitment_status': forms.Select(attrs={'class': 'form-select'}),
            'completedby_year': forms.Select(attrs={'class': 'form-select'}),
            'completedby_quarter': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_commitment_number(self):
        if not self.cleaned_data.get('commitment_number'):
            prefix = "COMMIT-"
            last_commitment = SystemPartnerCommitment.objects.order_by('commitment_number').last()
            if last_commitment:
                number_part = last_commitment.commitment_number.split('-')[2]
                new_number = int(number_part) + 1
            else:
                new_number = 1000  # Start from 1000
            return f"{prefix}{new_number}"
        return self.cleaned_data.get('commitment_number')

    def __init__(self, *args, **kwargs):
        super(PartnerActivityForm, self).__init__(*args, **kwargs)

        # Customize querysets for related fields
        self.fields['related_goal'].queryset = Goal.objects.all().order_by('goal_number')
        self.fields['related_objective'].queryset = Objective.objects.all().order_by('objective_number')
        self.fields['related_strategy'].queryset = Strategy.objects.all().order_by('strategy_number')

        # Concatenate goal_number with goal_name, and similar for objective and strategy
        self.fields['related_goal'].label_from_instance = lambda obj: f"Goal {obj.goal_number}: {obj.goal_name}"
        self.fields['related_objective'].label_from_instance = lambda obj: f"Obj. {obj.objective_number}: {obj.objective_name}"
        self.fields['related_strategy'].label_from_instance = lambda obj: f"{obj.strategy_number}: {obj.strategy_name}"


class NcffActivityForm(forms.ModelForm):
    ncff_team = forms.ModelChoiceField(
        queryset=NcffTeam.objects.all(),
        label="NCFF Team",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = NCActionStep
        exclude = ['activity_number', 'nc_staff_creator']  # Exclude fields that are set programmatically
        widgets = {
            'activity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'activity_lead': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_status': forms.Select(attrs={'class': 'form-select'}),
            'completedby_year': forms.Select(attrs={'class': 'form-select'}),
            'completedby_quarter': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(NcffActivityForm, self).__init__(*args, **kwargs)

        # Customize querysets for related fields if needed
        self.fields['related_goal'].queryset = Goal.objects.all().order_by('goal_number')
        self.fields['related_objective'].queryset = Objective.objects.all().order_by('objective_number')
        self.fields['related_strategy'].queryset = Strategy.objects.all().order_by('strategy_number')

        # Concatenate goal_number with goal_name, and similar for objective and strategy
        self.fields['related_goal'].label_from_instance = lambda obj: f"Goal {obj.goal_number}: {obj.goal_name}"
        self.fields['related_objective'].label_from_instance = lambda obj: f"Obj. {obj.objective_number}: {obj.objective_name}"
        self.fields['related_strategy'].label_from_instance = lambda obj: f"{obj.strategy_number}: {obj.strategy_name}"


# forms.py
class ActionStepsFilterForm(forms.Form):
    ACTOR_TYPES = [
        ('', 'All Actors'),
        ('nc', 'Nebraska Children'),
        ('community', 'Community Collaboratives'),
        ('partner', 'System Partners')
    ]

    actor_type = forms.ChoiceField(
        choices=ACTOR_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    actor = forms.ModelChoiceField(
        queryset=None,  # Will be set dynamically via JavaScript
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    related_goal = forms.ModelChoiceField(
        queryset=Goal.objects.all().order_by('goal_number'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    related_objective = forms.ModelChoiceField(
        queryset=Objective.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    related_strategy = forms.ModelChoiceField(
        queryset=Strategy.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    activity_status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + list(ActivityStatusChoice.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    completedby_year = forms.ChoiceField(
        choices=[('', 'All Years')] + list(Years.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    completedby_quarter = forms.ChoiceField(
        choices=[('', 'All Quarters')] + list(Quarters.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )