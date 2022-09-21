from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from recipe.models import Recipe
from django.contrib.auth.models import User
from recipe.views import UserRecipesListView


class RecipeListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe:recipe_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/list.html')


class UserRecipeListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create(username='user1', password='12345')
        self.recipe1 = Recipe.objects.create(name='test_recipe1',
                                             slug='test_recipe1',
                                             description='description for test recipe1',
                                             instructions='instructions for test recipe1',
                                             author=self.user1,
                                             )
        self.recipe2 = Recipe.objects.create(name='test_recipe2',
                                             slug='test_recipe2',
                                             description='description for test recipe2',
                                             instructions='instructions for test recipe2',
                                             author=self.user1,
                                             )
        self.user2 = User.objects.create(username='user2', password='12345')
        self.recipe3 = Recipe.objects.create(name='test_recipe3',
                                             slug='test_recipe3',
                                             description='description for test recipe3',
                                             instructions='instructions for test recipe3',
                                             author=self.user2,
                                             )

    def test_status_code(self):
        request = self.factory.get('/recipe/my_recipes')
        request.user = self.user1
        response = UserRecipesListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_get_queryset(self):
        request = self.factory.get('/recipe/my_recipes')
        request.user = self.user1
        response = UserRecipesListView.as_view()(request)
        qs = response.context_data['object_list']

        self.assertNotIn(self.recipe3, list(qs))
        self.assertEqual(len(qs), 2)


class RecipeDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='user1', password='12345')
        self.recipe = Recipe.objects.create(name='test_recipe',
                                            slug='test_recipe',
                                            description='description for test recipe',
                                            instructions='instructions for test recipe',
                                            author=self.user,
                                            )

    def test_details(self):
        response = self.client.get(reverse('recipe:recipe_detail',
                                           kwargs={'slug': self.recipe.slug, 'id': self.recipe.id}))

        self.assertEqual(response.status_code, 200)
