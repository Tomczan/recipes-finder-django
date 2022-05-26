from django import views
from django.shortcuts import render
from recipe.models import Integrent, IntegrentType, Recipe
from recipe.serializers import IntegrentSerializer, IntegrentTypeSerializer, RecipeSerializer
from rest_framework import viewsets

# Create your views here.


class IntegrentTypeViewSet(viewsets.ModelViewSet):
    queryset = IntegrentType.objects.all()
    serializer_class = IntegrentTypeSerializer


class IntegrentViewSet(viewsets.ModelViewSet):
    queryset = Integrent.objects.all()
    serializer_class = IntegrentSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
