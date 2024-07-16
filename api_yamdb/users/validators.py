from django.core.exceptions import ValidationError
from django.conf import settings


def validate_username(value):
    if value in settings.STOP_LIST:
        raise ValidationError(f'Имя "{value}" использовать нельзя')
