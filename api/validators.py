from datetime import datetime

from django.core.exceptions import ValidationError


def custom_year_validator(title_year):
    if title_year > datetime.now().year:
        raise ValidationError(
            f'{title_year} год больше текущего',
            code='invalid',
        )
