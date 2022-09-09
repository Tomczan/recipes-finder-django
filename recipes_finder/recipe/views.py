from account.forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView

from .forms import RecipeCreateForm, RecipeIngredientsForm
from .models import Recipe, RecipeIngredients

# Create your views here.


def home(request):
    login_form = LoginForm(request.POST)
    return render(request, "home.html", {'login_form': login_form})


def recipe_list_view(request):
    recipes = Recipe.objects.all()
    return render(request,
                  'recipe/list.html',
                  {'recipes': recipes})


def recipe_detail_view(request, slug, id):
    recipe = get_object_or_404(Recipe, slug=slug, id=id)
    return render(request,
                  'recipe/detail.html',
                  {'recipe': recipe})


@login_required
def recipe_update_view(request, slug, id):
    IngredientInlineFormSet = inlineformset_factory(Recipe,
                                                    RecipeIngredients,
                                                    form=RecipeIngredientsForm,
                                                    extra=0,
                                                    can_delete=False)
    recipe = get_object_or_404(Recipe, slug=slug, id=id)
    if request.user != recipe.author:
        return redirect('recipe:recipe_list')
    recipe_form = RecipeCreateForm(request.POST or None,
                                   instance=recipe)
    qs = RecipeIngredients.objects.filter(recipe=recipe)
    formset = IngredientInlineFormSet(request.POST or None,
                                      instance=recipe,
                                      queryset=qs)
    if recipe_form.is_valid() and formset.is_valid():
        recipe.save()
        formset = formset.cleaned_data
        for form in formset:
            if form:
                ingredient = RecipeIngredients(quantity=form['quantity'],
                                               unit=form['unit'],
                                               ingredient=form['ingredient'],
                                               recipe=recipe)
                ingredient.save()
        messages.success(
            request, f'The recipe "{recipe.name}" has been edited.')
        return redirect('recipe:recipe_list')
    template_name = 'recipe/update.html'
    context = {
        "recipe": recipe,
        "form": recipe_form,
        "formset": formset
    }
    return render(request, template_name, context)


@login_required
def recipe_create_view(request):
    IngredientInlineFormSet = inlineformset_factory(Recipe,
                                                    RecipeIngredients,
                                                    form=RecipeIngredientsForm,
                                                    extra=0,
                                                    can_delete=False)
    recipe_form = RecipeCreateForm(request.POST or None)
    formset = IngredientInlineFormSet(request.POST or None)
    if recipe_form.is_valid() and formset.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        formset = formset.cleaned_data
        for form in formset:
            if form:
                ingredient = RecipeIngredients(quantity=form['quantity'],
                                               unit=form['unit'],
                                               ingredient=form['ingredient'],
                                               recipe=recipe)
                ingredient.save()
        messages.success(
            request, f'The recipe "{recipe.name}" has been added.')
        return redirect('recipe:recipe_create')
    template_name = 'recipe/create.html'
    context = {
        "form": recipe_form,
        "formset": formset
    }
    return render(request, template_name, context)


class UserRecipesListView(ListView):
    model = Recipe
    template_name: str = 'my_recipes.html'
    paginate_by: int = 20

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)
