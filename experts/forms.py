from django import forms
from .models import Expert

class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['bio', 'experience', 'price_per_hour']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
