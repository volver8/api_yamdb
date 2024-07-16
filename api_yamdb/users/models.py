from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from .constants import MAX_LENGTH
from .validators import validate_username


class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    username = models.CharField(
        validators=[UnicodeUsernameValidator(), validate_username],
        max_length=MAX_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH,
        choices=RoleChoice.choices,
        default=RoleChoice.USER,
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH,
        blank=True
    )

    @property
    def is_admin(self):
        return (
            self.role == self.RoleChoice.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return (
            self.role == self.RoleChoice.MODERATOR
            or self.is_superuser
        )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
