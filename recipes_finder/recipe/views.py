from account.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.contrib import messages

from .forms import RecipeCreateForm, RecipeIngredientsForm
from .models import Recipe, RecipeIngredients

# Create your views here.


def home(request):
    login_form = LoginForm(request.POST)
    return render(request, "home.html", {'login_form': login_form})


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


class RecipeCreateView(LoginRequiredMixin, CreateView):
    form_class = RecipeCreateForm
    template_name = 'recipe/create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        # obj.save()
        return super().form_valid(form)


@login_required
def recipe_create(request):
    IngredientInlineFormSet = inlineformset_factory(Recipe,
                                                    RecipeIngredients, form=RecipeIngredientsForm, extra=1)
    if request.method == 'POST':
        recipe_form = RecipeCreateForm(request.POST)
        formset = IngredientInlineFormSet(request.POST)
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            formset = formset.cleaned_data
            for i in formset:
                try:
                    ingredient = RecipeIngredients(quantity=i['quantity'], unit=i['unit'],
                                                   ingredient=i['ingredient'], recipe=recipe)
                    ingredient.save()
                except:
                    print(
                        f'Cannot add ingredient to the recipe from this form: {i}')
            messages.success(
                request, f'The recipe "{recipe.name}" has been added.')
            return redirect('recipe:recipe_create')

    recipe_form = RecipeCreateForm()
    formset = IngredientInlineFormSet()
    template_name = 'recipe/create.html'
    context = {
        "form": recipe_form,
        "formset": formset
    }
    return render(request, template_name, context)
