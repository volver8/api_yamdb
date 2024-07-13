from django.db import models

from users.models import User


NAME_LEN = 256
SLUG_LEN = 50


class NameModel(models.Model):
    """Модель поля имени."""

    name = models.CharField('Название', max_length=NAME_LEN)  # type:ignore

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SlugModel(NameModel):
    """Модель поля слага."""

    slug = models.SlugField(
        'Идентификатор',
        max_length=SLUG_LEN,
        unique=True,
        help_text='Идентификатор; разрешены символы '
        'латиницы, цифры, дефис и подчёркивание.'
    )  # type:ignore

    class Meta:
        abstract = True


class Category(SlugModel):
    """Модель категории произведения."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(SlugModel):
    """Модель жанра произведения."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):
    """Модель произведения."""

    year = models.PositiveSmallIntegerField('Год произведения')  # type:ignore
    rating = models.SmallIntegerField('Рейтинг произведения')  # type:ignore
    description = models.TextField(
        'Описание комментария',
        blank=True,
        null=True
    )  # type:ignore
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр публикации',
        related_name='titles'
    )  # type:ignore
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


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
