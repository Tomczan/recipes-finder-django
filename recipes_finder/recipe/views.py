from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

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

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs['id'], slug=self.kwargs['slug'])


class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'recipe/create.html'
    IngredientInlineFormSet = inlineformset_factory(Recipe,
                                                    RecipeIngredients,
                                                    form=RecipeIngredientsForm,
                                                    extra=0,
                                                    can_delete=False)

    def get(self, request):
        recipe_form = RecipeCreateForm()
        formset = self.IngredientInlineFormSet()
        context = {
            "form": recipe_form,
            "formset": formset
        }
        return render(request, self.template_name, context)

    def post(self, request):
        recipe_form = RecipeCreateForm(request.POST)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            formset = self.IngredientInlineFormSet(request.POST,
                                                   instance=recipe)
            if formset.is_valid():
                recipe.author = request.user
                recipe.save()
                formset.save()
            messages.success(
                request, f'The recipe "{recipe.name}" has been added.')
        return redirect('recipe:recipe_create')


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name', 'description', 'instructions']
    template_name = 'recipe/update.html'
    IngredientInlineFormSet = inlineformset_factory(Recipe,
                                                    RecipeIngredients,
                                                    form=RecipeIngredientsForm,
                                                    extra=0,
                                                    can_delete=False)

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        if request.user != self.object.author:
            messages.warning(
                request, 'You can not edit a recipe that is not yours.')
            return redirect('recipe:recipe_list')

        recipe_form = RecipeCreateForm(instance=self.object)
        qs = RecipeIngredients.objects.filter(recipe=self.object)
        formset = self.IngredientInlineFormSet(instance=self.object,
                                               queryset=qs)
        context = {
            "form": recipe_form,
            "formset": formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        recipe_form = RecipeCreateForm(request.POST,
                                       instance=self.object)
        formset = self.IngredientInlineFormSet(request.POST,
                                               instance=self.object)
        if recipe_form.is_valid() and formset.is_valid():
            recipe_form.save()
            formset.save()
            messages.success(
                request, f'The recipe "{self.object}" has been edited.')
        return redirect('recipe:recipe_list')

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs['id'])


class RecipeToApproveListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('recipe.add_recipe',
                           'recipe.view_recipe',
                           'recipe.change_recipe')
    model = Recipe
    template_name = 'recipe/to_approve.html'
    paginate_by = 1

    def get_queryset(self):
        return Recipe.objects.filter(status='unapproved')

    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        if 'approve' in request.POST:
            recipe.status = request.POST.get('approve')
            recipe.save()
            messages.success(
                request, f'The recipe "{recipe.name}" has been approved.')
        if 'decline' in request.POST:
            recipe.status = request.POST.get('decline')
            recipe.save()
            messages.success(
                request, f'The recipe "{recipe.name}" has been declined.')
        return redirect('recipe:recipes_to_approve')
