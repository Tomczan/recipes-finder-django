from django.urls import path
from .views import home, recipe_list, recipe_detail, RecipeCreateView, recipe_create

app_name = 'recipe'

urlpatterns = [
    path('recipe/', recipe_list, name='recipe_list'),
    path('recipe/create', recipe_create, name='recipe_create'),
    path('recipe/<slug:slug>/<int:id>',
         recipe_detail, name='recipe_detail'),
    path('', home, name='home'),
]
