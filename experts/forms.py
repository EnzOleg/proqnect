# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Expert, ExpertSkill

class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['specialization', 'bio', 'experience', 'price_per_hour']

# Создаем inline formset для модели ExpertSkill, связанной с Expert
ExpertSkillFormSet = inlineformset_factory(
    parent_model=Expert,
    model=ExpertSkill,
    fields=['name'],      # какие поля хотим редактировать
    extra=3,             # сколько «пустых» форм для добавления новых навыков
    can_delete=True      # можно ли удалять уже добавленные навыки
)
