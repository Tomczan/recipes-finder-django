from django.urls import path
from .views import *

app_name = 'recipe'

urlpatterns = [
    path('recipe/', RecipeList.as_view(), name='recipe_list'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<slug:slug>/<int:id>/update/',
         RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<slug:slug>/<int:id>/',
         RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/my_recipes/', UserRecipesListView.as_view(), name='my_recipes'),
    path('recipe/staff/recipe_to_approve/<int:id>/',
         RecipeToApproveListView.as_view(), name='recipes_to_approve'),
    path('recipe/staff/recipe_to_approve/',
         RecipeToApproveListView.as_view(), name='recipes_to_approve'),
    #     path('recipe/staff/approve_or_decline/',
    #          RecipeApproveOrDecline.as_view(), name='approve_or_decline'),
    path('', home, name='home'),
]
