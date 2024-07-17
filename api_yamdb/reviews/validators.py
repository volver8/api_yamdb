from django.core.exceptions import ValidationError
from datetime import datetime as dt


def validation_year(value):
    if value > dt.now().year:
        raise ValidationError(
            f'Год выпуска не может быть больше текущего: {dt.now().year}'
        )
