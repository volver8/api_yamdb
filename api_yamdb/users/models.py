from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username
from reviews.constants import (USERNAME_LENGTH,
                               EMAIL_LEHGTH, ROLES, USER,
                               USERNAME_LENGTH)



class User(AbstractUser):

    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=[validate_username],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=EMAIL_LEHGTH,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(ROLES[1]) for ROLES in ROLES),
        choices=ROLES,
        default=USER,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=USERNAME_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=USERNAME_LENGTH,
        blank=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
