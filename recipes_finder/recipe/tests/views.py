from django.test import TestCase, Client
from django.urls import reverse
from recipe.models import Ingredient, IngredientType, Recipe, RecipeIngredients
from django.contrib.auth.models import User


class RecipeListViewTestCase(TestCase):
    def test_recipe_list_view(self):
        client = Client()

        response = client.get(reverse('recipe:recipe_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/list.html')


class RecipeDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', password='12345')
        self.recipe = Recipe.objects.create(name='test_recipe',
                                            slug='test_recipe',
                                            description='description for test recipe',
                                            instructions='instructions for test recipe',
                                            author=self.user,
                                            )

    def test_recipe_detail_view(self):
        client = Client()

        response = client.get(reverse('recipe:recipe_detail',
                                      kwargs={'slug': self.recipe.slug, 'id': self.recipe.id}))

        self.assertEqual(response.status_code, 200)
