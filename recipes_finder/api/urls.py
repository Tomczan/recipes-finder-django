from django.urls import path, include
from rest_framework import routers
from .views import IngredientViewSet, IngredientTypeViewSet, RecipeViewSet, IngredientTypeGenericView

router = routers.DefaultRouter()
router.register(r'viewset/ingredients', IngredientViewSet)
router.register(r'viewset/ingredient-type', IngredientTypeViewSet)
router.register(r'viewset/recipe', RecipeViewSet)

urlpatterns = [
    path('ingredient-type/', IngredientTypeGenericView.as_view(),
         name='ingredient_type'),
    path('', include(router.urls)),
]
