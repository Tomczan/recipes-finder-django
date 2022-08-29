from rest_framework import serializers
from recipe.models import Ingredient, IngredientType, Recipe, RecipeIngredients


class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = ['name']


class IngredientSerializer(serializers.ModelSerializer):
    type = IngredientTypeSerializer()

    class Meta:
        model = Ingredient
        fields = ['name', 'prefered_unit', 'type']


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredients
        fields = ['quantity', 'unit', 'ingredient']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientsSerializer(
        source='recipe_to_ingredient', read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'instructions', 'ingredients']
