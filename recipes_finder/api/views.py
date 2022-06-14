from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render
from recipe.models import Ingredient, IngredientType, Recipe
from recipe.serializers import (IngredientSerializer, IngredientTypeSerializer,
                                RecipeSerializer)
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from .serializers import UserSerializer
# Create your views here.


class IngredientTypeViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    permission_classes = [IsAdminUser]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminUser]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAdminUser]


class IngredientTypeGenericView(generics.ListAPIView):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CreateUserView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
