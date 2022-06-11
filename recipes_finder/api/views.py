from django import views
from django.shortcuts import render
from recipe.models import Ingredient, IngredientType, Recipe
from recipe.serializers import (
    IngredientSerializer, IngredientTypeSerializer, RecipeSerializer
)
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class IngredientTypeViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class IngredientTypeGenericView(generics.ListAPIView):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer