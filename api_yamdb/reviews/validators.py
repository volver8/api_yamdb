from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validation_year(value):
    current_year = dt.now().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше текущего: {current_year}'
        )
