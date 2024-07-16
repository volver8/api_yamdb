from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import NAME_LEN, SLUG_LEN
from .validators import validation_year


User = get_user_model()


class NameModel(models.Model):
    """Модель поля имени."""

    name = models.CharField('Название', max_length=NAME_LEN)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SlugModel(models.Model):
    """Модель поля слага."""

    slug = models.SlugField(
        'Идентификатор',
        max_length=SLUG_LEN,
        unique=True,
        help_text='Идентификатор; разрешены символы '
        'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        abstract = True


class Category(NameModel, SlugModel):
    """Модель категории произведения."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(NameModel, SlugModel):
    """Модель жанра произведения."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(NameModel):
    """Модель произведения."""

    year = models.IntegerField(
        'Год произведения',
        validators=(validation_year, )
    )
    description = models.TextField(
        'Описание комментария',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория публикации',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = [
            '-year',
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""
    
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10, message='Оценка не может быть выше 10!'),
            MinValueValidator(1, message='Оценка не может быть ниже 1!')]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария."""
    
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
