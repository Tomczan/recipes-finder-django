from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

UNIT_CHOICES = [
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('ml', 'mililitr'),
    ('l', 'litr'),
]


class IngredientType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    prefered_unit = models.CharField(
        max_length=2, choices=UNIT_CHOICES, blank=False)
    type = models.ForeignKey(IngredientType, on_delete=models.PROTECT)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Approved'),
        ('unapproved', 'Unapproved'),
        ('hidden', 'Hidden')
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200, unique_for_date='created', blank=True)
    description = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='unapproved')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredients', blank=True)
    objects = models.Manager()  # default Manager
    tags = TaggableManager()  # taggit

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipe:recipe_detail",
                       args=[self.slug,
                             self.id])


class RecipeIngredients(models.Model):
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=False)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name='ingredient_to_recipe')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_to_ingredient')

    class Meta:
        unique_together = ('ingredient', 'recipe')

    def __str__(self) -> str:
        return self.ingredient.name
