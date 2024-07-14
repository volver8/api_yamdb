from django.db import models
from django.contrib.auth import get_user_model


NAME_LEN = 256
SLUG_LEN = 50


User = get_user_model()


class NameModel(models.Model):
    """Модель поля имени."""

    name = models.CharField('Название', max_length=NAME_LEN)

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
    )

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
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = [
            '-year',
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)


class Comment(models.Model):
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
