from django import forms
from django.forms import ModelForm
from .models import CommunityActivity, StrategyActivity, Goal, Objective, Strategy
from django.db.models import F


class CommunityActivityForm(forms.ModelForm):
    class Meta:
        model = CommunityActivity
        fields = '__all__'
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
        # Set empty_label for choice fields if you want a placeholder
        self.fields['completedby_year'].empty_label = "Select Year"
        self.fields['completedby_quarter'].empty_label = "Select Quarter"

        # Bootstrap row for specific fields
        self.fields['activity_status'].widget.attrs.update({'class': 'form-control col-md-4'})
        self.fields['completedby_year'].widget.attrs.update({'class': 'form-control col-md-4'})
        self.fields['completedby_quarter'].widget.attrs.update({'class': 'form-control col-md-4'})
        self.fields['completedby_year'].widget.attrs.update({'class': 'form-select'})
        self.fields['completedby_quarter'].widget.attrs.update({'class': 'form-select'})

        # Customize the related_goal field
        self.fields['related_goal'].queryset = Goal.objects.annotate(
            custom_label=F('goal_name')
        ).order_by('goal_number')

        self.fields['related_objective'].queryset = Objective.objects.annotate(
            custom_label=F('objective_name')
        ).order_by('objective_number')

        self.fields['related_strategy'].queryset = Strategy.objects.annotate(
            custom_label=F('strategy_name')
        ).order_by('strategy_number')

        # Override the label_from_instance method to use custom_label
        self.fields['related_goal'].label_from_instance = lambda obj: getattr(obj, 'custom_label', obj.goal_name)
        self.fields['related_objective'].label_from_instance = lambda obj: (
            getattr(obj, 'custom_label', obj.objective_name))
        self.fields['related_strategy'].label_from_instance = lambda obj: (
            getattr(obj, 'custom_label', obj.strategy_name))

        # Add a placeholder
        self.fields['related_collaborative'].choices = [('', 'Please select your Community Collaborative')] + list(
            self.fields['related_collaborative'].choices)
        self.fields['related_goal'].choices = [('', 'Please select the related Goal')] + list(
            self.fields['related_goal'].choices)
        self.fields['related_objective'].choices = [('', 'Please select the related Objective')] + list(
            self.fields['related_objective'].choices)
        self.fields['related_strategy'].choices = [('', 'Please select the related Strategy')] + list(
            self.fields['related_strategy'].choices)


class PartnerActivityForm(forms.ModelForm):
    class Meta:
        model = StrategyActivity
        fields = '__all__'
        widgets = {
            'activity_name': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_details': forms.Textarea(attrs={'class': 'form-control'}),
            'activity_lead': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_priority': forms.Select(attrs={'class': 'form-select'}),
            'activity_status': forms.Select(attrs={'class': 'form-select'}),
            'completedby_year': forms.Select(attrs={'class': 'form-select'}),
            'completedby_quarter': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(PartnerActivityForm, self).__init__(*args, **kwargs)
        # Bootstrap row for specific fields
        self.fields['activity_status'].widget.attrs.update({'class': 'form-control col-md-4'}),
        self.fields['completedby_year'].widget.attrs.update({'class': 'form-control col-md-4'}),
        self.fields['completedby_quarter'].widget.attrs.update({'class': 'form-control col-md-4'})
