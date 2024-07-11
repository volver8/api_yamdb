from django.db import models


NAME_LEN = 256
SLUG_LEN = 50


class Category(models.Model):
    """Модель категории произведения"""
    name = models.CharField('Название категории', max_length=NAME_LEN)
    slug = models.SlugField(
        'Идентификатор категории произведения',
        max_length = SLUG_LEN,
        unique=True,
        help_text='Идентификатор категории; разрешены '
        'символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
