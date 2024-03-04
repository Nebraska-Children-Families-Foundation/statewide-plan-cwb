from django import forms
from django.forms import ModelForm
from .models import CommunityActivity


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
        # Bootstrap row for specific fields
        self.fields['activity_status'].widget.attrs.update({'class': 'form-control col-md-4'})
        self.fields['completedby_year'].widget.attrs.update({'class': 'form-control col-md-4'})
        self.fields['completedby_quarter'].widget.attrs.update({'class': 'form-control col-md-4'})
