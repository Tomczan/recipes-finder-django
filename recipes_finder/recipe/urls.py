from django.urls import path
from .views import home, recipe_list, recipe_detail

app_name = 'recipe'

urlpatterns = [
    path('recipe/', recipe_list, name='recipe_list'),
    path('recipe/<int:year>/<int:month>/<int:day>/<slug:recipe>/',
         recipe_detail, name='recipe_detail'),
    path('', home, name='home'),
]
