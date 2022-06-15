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


def recipe_detail(request, year, month, day, recipe):
    recipe = get_object_or_404(Recipe, slug=recipe,
                               is_visible=True,
                               created__year=year,
                               created__month=month,
                               created__day=day)
    return render(request,
                  'recipe/detail.html',
                  {'recipe': recipe})
