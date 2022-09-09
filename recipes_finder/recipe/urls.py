from django.urls import path
from .views import *

app_name = 'recipe'

urlpatterns = [
    path('recipe/', recipe_list_view, name='recipe_list'),
    path('recipe/create', recipe_create_view, name='recipe_create'),
    path('recipe/update/<int:id>',
         recipe_update_view, name='recipe_update'),
    path('recipe/<slug:slug>/<int:id>',
         recipe_detail_view, name='recipe_detail'),
    path('my_recipes/', UserRecipesListView.as_view(), name='my_recipes'),
    path('', home, name='home'),
]
