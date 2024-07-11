from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import (MAX_LENGTH, ADMIN, MODERATOR,
                        EMAIL_LEHGTH, ROLES, USER)



class User(AbstractUser):

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=EMAIL_LEHGTH,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=MAX_LENGTH,
        choices=ROLES,
        default=USER,
        blank=True
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
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=MAX_LENGTH,
        null=True
    )

    @property
    def is_user(self):
        return self.role == USER
    
    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
    
    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
