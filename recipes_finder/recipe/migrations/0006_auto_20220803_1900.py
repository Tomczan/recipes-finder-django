# Generated by Django 3.2 on 2022-08-03 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20220615_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='is_visible',
        ),
        migrations.AddField(
            model_name='recipe',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('hidden', 'Hidden')], default='draft', max_length=10),
        ),
    ]
