from django.db import models



class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name
