from django.db import models

# Create your models here.
# https://github.com/dgrant/django_recipes/blob/ff68768fd3b1282f02bae3a041e624b8d5338f16/recipes/models.py#L319

UNIT_CHOICES = [
    ('g', 'gram'),
    ('kg', 'kilogram'),
    ('ml', 'mililitr'),
    ('l', 'litr'),
]


class IntegrentType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Integrent(models.Model):
    name = models.CharField(max_length=200)
    prefered_unit = models.CharField(
        max_length=2, choices=UNIT_CHOICES, blank=False)
    type = models.ForeignKey(IntegrentType, on_delete=models.PROTECT)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    # image = models.ImageField(
    #     upload_to='recipes/%Y/%m/%d', height_field=None, width_field=None, max_length=100)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_visible = models.BooleanField(default=False)
    integrents = models.ManyToManyField(Integrent, through='RecipeIntegrents')

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.name

# TODO: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ManyToManyField.through
# add: UniqueConstraint


class RecipeIntegrents(models.Model):
    amount = models.IntegerField(default=0)
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, blank=False)
    integrent = models.ForeignKey(
        Integrent, on_delete=models.PROTECT, related_name='integrent_to_recipe')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_to_integrent')

    def __str__(self) -> str:
        return self.integrent.name
