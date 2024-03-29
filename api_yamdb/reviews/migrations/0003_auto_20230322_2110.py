# Generated by Django 3.2 on 2023-03-22 18:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230322_1953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'default_related_name': 'categories', 'ordering': ['name'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'default_related_name': 'genres', 'ordering': ['name'], 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'ordering': ['-year'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2023)], verbose_name='Год выпуска'),
        ),
    ]
