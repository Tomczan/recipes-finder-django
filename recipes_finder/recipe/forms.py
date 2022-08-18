from django.contrib.auth.models import User
from django.forms import ModelForm

from recipe.models import Recipe


class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'ingredients']
