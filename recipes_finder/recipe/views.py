from django.shortcuts import get_object_or_404, render

from .models import Recipe

# Create your views here.


def home(request):    
    return render(request, "home.html")


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request,
                  'recipe/list.html',
                  {'recipes': recipes})


def recipe_detail(request, slug, id):
    recipe = get_object_or_404(Recipe, slug=slug, id=id)
    return render(request,
                  'recipe/detail.html',
                  {'recipe': recipe})
