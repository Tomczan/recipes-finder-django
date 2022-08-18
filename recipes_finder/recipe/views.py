from account.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView

from .forms import RecipeCreateForm
from .models import Recipe, IngredientType

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
