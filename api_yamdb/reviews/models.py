from django.db import models
from django.core import validators

NAME_LEN = 256
SLUG_LEN = 50


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        'Название',
        max_length=NAME_LEN
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=SLUG_LEN,
        unique=True,
        validators=[validators.RegexValidator(regex=r'^[\w.@+\- ]+$'),],
        help_text='Идентификатор; разрешены символы '
        'латиницы, цифры, дефис и подчёркивание.'
    )  

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        'Название',
        max_length=NAME_LEN
        )
    slug = models.SlugField(
        'Идентификатор',
        max_length=SLUG_LEN,
        unique=True,
        help_text='Идентификатор; разрешены символы '
        'латиницы, цифры, дефис и подчёркивание.'
    )  # type:ignore

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название',
        max_length=NAME_LEN
    )
    year = models.IntegerField('Год произведения')
    description = models.TextField(
        'Описание комментария',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория публикации',
        related_name='titles'
    )  # type:ignore

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = [
            '-year',
            'name',
            'genre__slug',
            'category__slug',
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)  # type:ignore
    title = models.ForeignKey(Title, on_delete=models.CASCADE)  # type:ignore
