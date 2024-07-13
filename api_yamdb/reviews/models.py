from django.db import models
from django.contrib.auth import get_user_model


NAME_LEN = 256
SLUG_LEN = 50


User = get_user_model()


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

    def __str__(self):
        return self.name


class Genre(SlugModel):
    """Модель жанра произведения."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(NameModel):
    """Модель произведения."""

    year = models.PositiveSmallIntegerField('Год произведения')  # type:ignore
    description = models.TextField(
        'Описание комментария',
        blank=True,
        null=True
    )  # type:ignore
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle"
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

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)  # type:ignore
    title = models.ForeignKey(Title, on_delete=models.CASCADE)  # type:ignore


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )  # type:ignore

    text = models.TextField()  # type:ignore
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )  # type:ignore
    score = models.IntegerField()  # type:ignore
    pub_date = models.DateTimeField(auto_now_add=True)  # type:ignore

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
