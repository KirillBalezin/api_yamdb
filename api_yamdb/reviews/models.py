from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)


MIN_YEAR = 0
MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50
SCORE_MIN = 1
SCORE_MAX = 10
USER_NAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'administrator'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USER_NAME_MAX_LENGTH,
        null=True,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=USER_NAME_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=USER_NAME_MAX_LENGTH,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=(len(max(max(ROLES, key=len)))),
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]

    def __str__(self):
        return f'{self.username}'


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name="Название жанра"
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
        db_index=True,
        verbose_name="Slug жанра"
    )

    class Meta:
        ordering = ['name']
        default_related_name = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name="Название категории"
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG,
        db_index=True,
        verbose_name="Slug категории"
    )

    class Meta:
        ordering = ['name']
        default_related_name = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name="Название произведения"
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        validators=[MinValueValidator(MIN_YEAR),
                    MaxValueValidator(int(datetime.now().year))]
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория"
    )

    class Meta:
        ordering = ['-year']
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.ForeignKey(
        Title,
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
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(SCORE_MIN),
                    MaxValueValidator(SCORE_MAX)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
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

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
