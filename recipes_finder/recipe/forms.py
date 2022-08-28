from django.forms import ModelForm

from recipe.models import Recipe, RecipeIngredients


class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions']


class RecipeIngredientsForm(ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['quantity', 'unit', 'ingredient']
