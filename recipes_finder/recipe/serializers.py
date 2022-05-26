from rest_framework import serializers
from recipe.models import Integrent, IntegrentType, Recipe


class IntegrentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrentType
        fields = ['name']


class IntegrentSerializer(serializers.ModelSerializer):
    type = IntegrentTypeSerializer()

    class Meta:
        model = Integrent
        fields = ['name', 'prefered_unit', 'type']


class RecipeSerializer(serializers.ModelSerializer):
    integrents = IntegrentSerializer

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'instructions', 'integrents']
