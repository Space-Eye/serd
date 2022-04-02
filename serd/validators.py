from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import string

def validate_plz(value: str):
    if len(value) != 5:
        raise ValidationError(
            _('PLZ muss fünfstellig sein')
        )
    if not value.isdecimal():
        raise ValidationError(
            _('PLZ darf nur Ziffern enthalten')
        )

def validate_phone(value: str):
    if len(value) < 6:
        raise ValidationError(
            _('Telephonnumer muss mindestens sechstellig sein')
        )
    if value[0] != '0' and value[0] != '+':
        raise ValidationError(
            _('Telephonnummer muss mit + oder 0 beginnen')
        )
    allowed = set(string.digits + ' '+ '-')
    if not set(value[1:]) <= allowed:
        raise ValidationError(
            _('Ungültiges Zeichen in der Telephonnummer')
        )