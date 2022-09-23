from django.test import TestCase, RequestFactory
from django.urls import reverse
from recipe.models import Recipe, IngredientType, Ingredient
from django.contrib.auth.models import User
from recipe.views import UserRecipesListView


class RecipeListViewTestCase(TestCase):
    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe:recipe_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/list.html')


class UserRecipeListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('recipe:my_recipes')
        self.user1 = User.objects.create(username='user1', password='12345')
        self.recipe1 = Recipe.objects.create(name='test_recipe1',
                                             slug='test_recipe1',
                                             description='description for test recipe1',
                                             instructions='instructions for test recipe1',
                                             author=self.user1)
        self.recipe2 = Recipe.objects.create(name='test_recipe2',
                                             slug='test_recipe2',
                                             description='description for test recipe2',
                                             instructions='instructions for test recipe2',
                                             author=self.user1)
        self.user2 = User.objects.create(username='user2', password='12345')
        self.recipe3 = Recipe.objects.create(name='test_recipe3',
                                             slug='test_recipe3',
                                             description='description for test recipe3',
                                             instructions='instructions for test recipe3',
                                             author=self.user2)

    def test_status_code(self):
        request = self.factory.get(self.url)
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
        self.user = User.objects.create(username='user1', password='12345')
        self.recipe = Recipe.objects.create(name='test_recipe',
                                            slug='test_recipe',
                                            description='description for test recipe',
                                            instructions='instructions for test recipe',
                                            author=self.user)

    def test_details(self):
        response = self.client.get(reverse('recipe:recipe_detail',
                                           kwargs={'slug': self.recipe.slug, 'id': self.recipe.id}))

        self.assertEqual(response.status_code, 200)


class RecipeCreateViewTestCase(TestCase):
    def setUp(self):
        # In order to be able to login by using client:
        # - Create user, DO NOT SET password there
        #   because Django won't recognize it as properly hashed password.
        # - user self.user.set_password() to properly password.
        self.user = User.objects.create(username='user1')
        self.user.set_password('12345')
        self.user.save()
        self.url = reverse('recipe:recipe_create')
        self.ingredient_type = IngredientType.objects.create(
            name='type_for_tests')
        Ingredient.objects.create(
            id=1, name='Salami', prefered_unit='g', type=self.ingredient_type)
        Ingredient.objects.create(
            id=2, name='Tomato', prefered_unit='g', type=self.ingredient_type)

    def test_GET_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

    def test_GET_logged_in(self):
        self.client.login(username='user1', password='12345')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_POST_recipe_without_ingredients(self):
        self.client.login(username='user1', password='12345')
        response = self.client.post(self.url, {
            'name': ['Pizza'],
            'description': ['Pizza with salami'],
            'instructions': ['1. Order\r\n2.Eat'],
            'recipe_to_ingredient-TOTAL_FORMS': ['0'],
            'recipe_to_ingredient-INITIAL_FORMS': ['0'],
            'recipe_to_ingredient-MIN_NUM_FORMS': ['0'],
            'recipe_to_ingredient-MAX_NUM_FORMS': ['1000'],
            'recipe_to_ingredient-__prefix__-quantity': ['0'],
            'recipe_to_ingredient-__prefix__-unit': [''],
            'recipe_to_ingredient-__prefix__-ingredient': [''],
            'recipe_to_ingredient-__prefix__-recipe': [''],
            'recipe_to_ingredient-__prefix__-id': ['']
        })
        created_recipe = Recipe.objects.get(name='Pizza')
        ingredient_count = len(created_recipe.ingredients.all())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(created_recipe.name, 'Pizza')
        self.assertEqual(created_recipe.description, 'Pizza with salami')
        self.assertEqual(created_recipe.instructions, '1. Order\r\n2.Eat')
        self.assertEqual(ingredient_count, 0)

    def test_POST_recipe_with_2_ingredients(self):
        self.client.login(username='user1', password='12345')
        response = self.client.post(self.url, {
            'name': ['Pizza'],
            'description': ['Pizza with salami and tomatoes.'],
            'instructions': ['1. Example instructions...'],
            'recipe_to_ingredient-TOTAL_FORMS': ['2'],
            'recipe_to_ingredient-INITIAL_FORMS': ['0'],
            'recipe_to_ingredient-MIN_NUM_FORMS': ['0'],
            'recipe_to_ingredient-MAX_NUM_FORMS': ['1000'],
            'recipe_to_ingredient-0-quantity': ['300'],
            'recipe_to_ingredient-0-unit': ['g'],
            'recipe_to_ingredient-0-ingredient': ['1'],
            'recipe_to_ingredient-0-recipe': [''],
            'recipe_to_ingredient-0-id': [''],
            'recipe_to_ingredient-1-quantity': ['150'],
            'recipe_to_ingredient-1-unit': ['g'],
            'recipe_to_ingredient-1-ingredient': ['2'],
            'recipe_to_ingredient-1-recipe': [''],
            'recipe_to_ingredient-1-id': [''],
            'recipe_to_ingredient-__prefix__-quantity': ['0'],
            'recipe_to_ingredient-__prefix__-unit': [''],
            'recipe_to_ingredient-__prefix__-ingredient': [''],
            'recipe_to_ingredient-__prefix__-recipe': [''],
            'recipe_to_ingredient-__prefix__-id': ['']
        })
        created_recipe = Recipe.objects.get(name='Pizza')
        ingredient_count = len(created_recipe.ingredients.all())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(created_recipe.name, 'Pizza')
        self.assertEqual(created_recipe.description,
                         'Pizza with salami and tomatoes.')
        self.assertEqual(created_recipe.instructions,
                         '1. Example instructions...')
        self.assertEqual(ingredient_count, 2)
