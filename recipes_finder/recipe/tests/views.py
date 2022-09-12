from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from recipe.models import Recipe
from django.contrib.auth.models import User


class RecipeListViewTestCase(TestCase):
    def test_recipe_list_view(self):
        client = Client()

        response = client.get(reverse('recipe:recipe_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/list.html')


class UserRecipeListViewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='12345')
        self.recipe1 = Recipe.objects.create(name='test_recipe',
                                             slug='test_recipe',
                                             description='description for test recipe',
                                             instructions='instructions for test recipe',
                                             author=self.user1,
                                             )
        self.recipe2 = Recipe.objects.create(name='test_recipe',
                                             slug='test_recipe',
                                             description='description for test recipe',
                                             instructions='instructions for test recipe',
                                             author=self.user1,
                                             )
        self.user2 = User.objects.create(username='user2', password='12345')
        self.recipe3 = Recipe.objects.create(name='test_recipe',
                                             slug='test_recipe',
                                             description='description for test recipe',
                                             instructions='instructions for test recipe',
                                             author=self.user2,
                                             )

    def test_user_recipe_list_view(self):
        client = Client()

        # response =
        # DOKONCZ TEST


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
