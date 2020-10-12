import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ngettext


class IsAsciiValidator(object):
    def validate(self, password, user=None):
        if not password.isascii():
            raise ValidationError(
                _("Only English alphabet letters should be used"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Only English alphabet letters should be used")
        


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters"),
                code='password_too_short',
                params={'min_length': 8},
            )

    def get_help_text(self):
        return _("password must contain at least 8 characters")

class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("Password must contain at least one number, 0-9"),
                code='password_no_number'
            )

    def get_help_text(self):
        return _("Password must contain at least one number, 0-9")


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter, A-Z"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _("Password must contain at least one uppercase letter, A-Z")


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter, a-z."),
                code='password_no_lower',)

    def get_help_text(self):
        return _("Password must contain at least one lowercase letter, a-z.")


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("Password must contain at least one symbol: () [] {} | \ `~! @ # $% ^ & * _- + =;: '\", <> ./?"),
                code='password_no_symbol')

    def get_help_text(self):
        return _(_("Password must contain at least one symbol: () [] {} | \ `~! @ # $% ^ & * _- + =;: '\", <> ./?"))
