from django.core.exceptions import ValidationError

from .constants import CURRENT_YEAR


def validation_year(value):
    if value > CURRENT_YEAR:
        raise ValidationError(
            f'Год выпуска не может быть больше текущего: {CURRENT_YEAR}'
        )
