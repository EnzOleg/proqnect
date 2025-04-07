# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Expert, ExpertSkill, Review

class ExpertProfileForm(forms.ModelForm):
    specialization = forms.ChoiceField(choices=Expert.SPECIALIZATIONS, required=False, label="Специализация")
    custom_specialization = forms.CharField(required=False, label="Своя специализация" ,
                                            widget=forms.TextInput(attrs={"placeholder": "Введите свою специализацию"}))

    class Meta:
        model = Expert
        fields = ["specialization", "custom_specialization", "bio", "experience", "price_per_hour"]

ExpertSkillFormSet = inlineformset_factory(
    parent_model=Expert,
    model=ExpertSkill,
    fields=['name'],    
    extra=3,            
    can_delete=True     
)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(),
            "comment": forms.Textarea(attrs={"rows":4})
        }