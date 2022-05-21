from django.contrib import admin
from .models import Recipe, Integrent, IntegrentType, RecipeIntegrents

# Register your models here.


class RecipeIntegrentsInLine(admin.TabularInline):
    model = RecipeIntegrents
    extra = 1


@admin.register(IntegrentType)
class IntegrentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Integrent)
class IntegrentAdmin(admin.ModelAdmin):
    inlines = (RecipeIntegrentsInLine,)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIntegrentsInLine,)
