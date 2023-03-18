from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'reviews'
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'], name='unique_review')]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
