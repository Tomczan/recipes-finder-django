from django.test import TestCase, Client
from django.urls import reverse
from recipe.models import Ingredient, IngredientType, Recipe, RecipeIngredients


class RecipeViewsTestCase(TestCase):
    def test_recipe_list_view(self):
        client = Client()

        response = client.get(reverse('recipe:recipe_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/list.html')
