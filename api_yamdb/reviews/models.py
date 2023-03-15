from django.db import models



class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра"
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="Slug жанра"
    )

    class Meta:
        default_related_name = 'genres'

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории"
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="Slug категории"
    )

    class Meta:
        default_related_name = 'categories'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения"
    )
    year = models.IntegerField(
        verbose_name="Год выпуска"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenresTitles',
        verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Categories,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория"
    )

    class Meta:
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genre = models.ForeignKey(
        Genres,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre}: {self.title}'
