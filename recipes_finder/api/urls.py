from django.urls import path, include
from rest_framework import routers
from .views import IngredientViewSet, IngredientTypeViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'ingredient-type', IngredientTypeViewSet)
router.register(r'recipe', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
