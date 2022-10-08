from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import RecipeCreateForm, RecipeIngredientsForm
from .models import Recipe, RecipeIngredients

# Create your views here.


def home(request):
    return render(request, "home.html")


class RecipeList(ListView):
    model = Recipe
    template_name = 'recipe/list.html'
    paginate_by = 10

    def get_queryset(self):
        if 'query' in self.request.GET:
            query = self.request.GET['query']
            return Recipe.objects.annotate(similarity=TrigramSimilarity('name', query),).\
                filter(similarity__gt=0.1).order_by('-similarity')
        return super().get_queryset()


class UserRecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipe/my_recipes.html'
    paginate_by = 20

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/detail.html'

    def get_context_data(self, **kwargs):
        recipe_tags = self.object.tags.values_list('id', flat=True)
        similar_recipes = Recipe.objects.filter(
            tags__in=recipe_tags).exclude(id=self.object.id)
        similar_recipes = similar_recipes.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-updated')[:5]

        context = super().get_context_data(**kwargs)
        context['similar_recipes'] = similar_recipes

        return context


@ login_required
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


@ login_required
def recipe_update_view(request, slug, id):
    IngredientInlineFormSet = inlineformset_factory(Recipe,
                                                    RecipeIngredients,
                                                    form=RecipeIngredientsForm,
                                                    extra=0,
                                                    can_delete=False)
    recipe = get_object_or_404(Recipe, slug=slug, id=id)
    if request.user != recipe.author:
        messages.warning(
            request, 'You can not edit a recipe that is not yours.')
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
