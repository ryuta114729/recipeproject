from django import forms

from .models import Recipe
from .models import Review

class RecipeForm(forms.ModelForm):

    class Meta:
        
        model = Recipe

        fields = [
            'title',
            'ingredients',
            'cost',
            'instruction'
        ]

        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 6}),
            'seasonings': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 10}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = [
            'title',
            'rating',
            'comment'
        ]