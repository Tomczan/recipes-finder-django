# Generated by Django 3.2 on 2022-05-26 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_recipeintegrents_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='integrent',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='recipeintegrents',
            name='integrent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='integrent_to_recipe', to='recipe.integrent'),
        ),
        migrations.AlterField(
            model_name='recipeintegrents',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_to_integrent', to='recipe.recipe'),
        ),
    ]
