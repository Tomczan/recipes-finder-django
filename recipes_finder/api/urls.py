from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import (IngredientTypeGenericView, IngredientTypeViewSet,
                    IngredientViewSet, RecipeViewSet)


router = routers.DefaultRouter()
router.register(r'viewset/ingredients', IngredientViewSet)
router.register(r'viewset/ingredient-type', IngredientTypeViewSet)
router.register(r'viewset/recipe', RecipeViewSet)

urlpatterns = [
    path('ingredient-type/', IngredientTypeGenericView.as_view(),
         name='ingredient_type'),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
