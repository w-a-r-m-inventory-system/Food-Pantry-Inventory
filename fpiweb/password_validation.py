
from django.core.exceptions import ValidationError
from django.utils import timezone


class WarmInPasswordValidator:

    def validate(self, password, user=None):
        if 'warm' in password.lower():
            raise ValidationError("Password contains the word 'warm'")

    def get_help_text(self):
        return f"Your password cannot contain the word 'warm'"


class CurrentMonthInPasswordValidator:

    def validate(self, password, user=None):
        current_time = timezone.localtime()
        month_name = current_time.strftime('%B').lower()
        month_abbreviation = current_time.strftime('%b').lower()
        password = password.lower()
        if month_name in password or month_abbreviation in password:
            raise ValidationError("Password contains name of current month")

    def get_help_text(self):
        return f"Your password cannot contain the current month (either " \
               f"spelled out or abbreviated)"


class ShortPasswordValidator:

    def __init__(self, length_threshold=12):
        self.length_threshold = length_threshold

    def validate(self, password, user=None):
        if len(password) >= self.length_threshold:
            return
        has_upper_case = False
        has_lower_case = False
        has_digit = False
        for c in password:
            if not has_upper_case and c == c.upper():
                has_upper_case = True
            if not has_lower_case and c == c.lower():
                has_lower_case = True
            if not has_digit and c.isdigit():
                has_digit = True
        if all([has_upper_case, has_lower_case, has_digit]):
            return
        raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return f"Passwords under {self.length_threshold} characters must " \
               f"have: an uppercase character, a lowercase ""character, " \
               "and a digit"
