import re

from django.core.exceptions import ValidationError


def validate_unsubscribe_link(value):
    if value is None or value == '':
        return

    if len(re.findall(r'\{\{\s*unsubscribe_link\s*\}\}', value)) <= 0:
        raise ValidationError('Should include "{{ unsubscribe_link }}"')
