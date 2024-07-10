from django.core.exceptions import ValidationError
import re


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя "me" использовать нельзя)
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Запрещённые символы в имени пользователя'
        )