from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class LetterInPasswordValidator:
    def validate(self, password, user = None):
       if bool(re.search('[a-zA-Z]', password)) == False:
            raise ValidationError(_("Password must contain at least one letter."))

    def get_help_text(self):
        return _("Password must contain at least one letter.")


class NumberInPasswordValidator:
    def validate(self, password, user = None):
        if bool(re.search(r'\d', password)) == False:
            raise ValidationError(_("Password must contain at least one number."))

    def get_help_text(self):
        return _("Password must contain at least one number.")


class SpecialCharacterInPasswordValidator:
    special_characters = re.compile('[@_!#$%^&*()<>?/|}{~:]')

    def validate(self, password, user = None): 
        if self.special_characters.search(password) == None:
            raise ValidationError(_("Password must contain at least one special character."))

    def get_help_text(self):
        return _("Password must contain at least one special character.")
