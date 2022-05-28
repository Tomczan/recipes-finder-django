from django import views
from django.shortcuts import render
from recipe.models import Ingredient, IngredientType, Recipe
from recipe.serializers import (
    IngredientSerializer, IngredientTypeSerializer, RecipeSerializer
)
from rest_framework import viewsets

# Create your views here.


class IngredientTypeViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
