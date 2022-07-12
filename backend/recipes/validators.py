import re

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def validate_hex_code(value):
    reg = re.compile(r'^#(\d{6})$')
    if not reg.match(value):
        raise ValidationError('%s HEX code of color does not comply' % value)


LIMIT_MIN_INT = [MinValueValidator(1)]
