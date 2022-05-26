from rest_framework import serializers
from recipe.models import Integrent, IntegrentType, Recipe, RecipeIntegrents


class IntegrentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrentType
        fields = ['name']


class IntegrentSerializer(serializers.ModelSerializer):
    type = IntegrentTypeSerializer()

    class Meta:
        model = Integrent
        fields = ['name', 'prefered_unit', 'type']


class RecipeIntegrentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeIntegrents
        fields = ['amount', 'unit', 'integrent']


class RecipeSerializer(serializers.ModelSerializer):
    integrents = RecipeIntegrentsSerializer(
        source='recipe_to_integrent', read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'instructions', 'integrents']
