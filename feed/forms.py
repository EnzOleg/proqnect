# forms.py

from django import forms
from .models import Post

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
