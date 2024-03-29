from django.contrib.auth.models import User
from django.test import TestCase
from recipe.models import Ingredient, IngredientType, Recipe, RecipeIngredients


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', password='12345')
        self.ingredient_type = IngredientType.objects.create(name='vegetable')
        self.ingredient1 = Ingredient.objects.create(name='onion',
                                                     prefered_unit='g',
                                                     type=self.ingredient_type)
        self.ingredient2 = Ingredient.objects.create(name='paprika',
                                                     prefered_unit='g',
                                                     type=self.ingredient_type)
        self.recipe = Recipe.objects.create(name='test_recipe',
                                            slug='test_recipe',
                                            description='description for test recipe',
                                            instructions='instructions for test recipe',
                                            author=self.user)
        self.recipe_ingredient1 = RecipeIngredients(quantity=120,
                                                    unit='g',
                                                    ingredient=self.ingredient1,
                                                    recipe=self.recipe)
        self.recipe_ingredient1.save()

    def test_model_ingredient_type_str(self):
        self.assertEqual(str(self.ingredient_type), 'vegetable')
        self.assertNotEqual(str(self.ingredient_type), 'vegeteble')

    def test_model_ingredient_str(self):
        self.assertEqual(str(self.ingredient1), 'onion')
        self.assertEqual(str(self.ingredient2), 'paprika')
        self.assertNotEqual(str(self.ingredient1), 'paprika')

    def test_model_recipe_ingredient_str(self):
        self.assertEqual(str(self.recipe_ingredient1),
                         'test_recipe: onion 120g')

    def test_model_recipe_str(self):
        self.assertEqual(str(self.recipe), 'test_recipe')

    def test_model_recipe_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(),
                         f'/recipe/{self.recipe.slug}/{self.recipe.id}/')

    def test_model_recipe_slugify_on_save(self):
        self.recipe2 = Recipe.objects.create(name='Test-3_5AZaz/!@#$%^&*(/ Y€s',
                                             description='description',
                                             instructions='instructions',
                                             author=self.user)

        self.assertEqual(self.recipe2.slug, 'test-3_5azaz-ys')
        self.assertNotEqual(self.recipe2.slug, self.recipe2.name)
        self.assertNotEqual(self.recipe2.slug, 'test-3_5azaz/!@#$%^&*(/ y€s')
