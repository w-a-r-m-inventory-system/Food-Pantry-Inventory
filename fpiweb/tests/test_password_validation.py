

from django.conf import settings
from django.contrib.auth.password_validation import \
    get_password_validators, \
    validate_password
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from fpiweb.tests.utility import create_user


class PasswordValidationTest(TestCase):

    @staticmethod
    def validate(password, user=None):
        password_validators = get_password_validators(
            settings.AUTH_PASSWORD_VALIDATORS,
        )
        try:
            validate_password(
                password,
                user=user,
                password_validators=password_validators,
            )
        except ValidationError as error:
            return error.messages
        else:
            return []

    def test_password_validation(self):

        user = create_user(
            username='carol.smith',
            first_name='Carol',
            last_name='Smith',
            title='Ms.',
        )

        self.assertIn(
            'The password is too similar to the username.',
            self.validate('carol.smith', user),
        )

        self.assertIn(
            'This password is too short. It must contain at least 8 characters.',
            self.validate('aB3b8e'),
        )

        self.assertIn(
            'This password is too common.',
            self.validate('abcdefghi'),
        )

        self.assertIn(
            'This password is entirely numeric.',
            self.validate('198268756789'),
        )

        self.assertIn(
            "Password contains the word 'warm'",
            self.validate('kdovupwarm')
        )

        self.assertIn(
            "This password is too common.",
            self.validate("password"),
        )

        current_time = timezone.localtime()
        if all([
            current_time.hour == 23,
            current_time.minute == 59,
            current_time.second > 55,
        ]):
            self.fail("Too close to midnight to run this test")

        month_name = current_time.strftime('%B')
        month_abbreviation = current_time.strftime('%b')

        self.assertIn(
            "Password contains name of current month",
            self.validate(f'kdovup{month_abbreviation}')
        )

        self.assertIn(
            "Password contains name of current month",
            self.validate(f'kdovup{month_abbreviation.lower()}')
        )

        self.assertIn(
            "Password contains name of current month",
            self.validate(f'kdovup{month_name.lower()}')
        )

        validator_name = "ShortPasswordValidator"
        validator_config = None
        for config in settings.AUTH_PASSWORD_VALIDATORS:
            if validator_name in config['NAME']:
                validator_config = config
                break
        self.assertIsNotNone(
            validator_config,
            f"{validator_name} not found in settings.AUTH_PASSWORD_VALIDATORS",
        )

        length_threshold = validator_config.get(
            'OPTIONS', {}
        ).get('length_threshold')
        self.assertTrue(length_threshold, 'length_threshold option not found')

        error_message = f"Passwords under {length_threshold} characters must " \
                        f"have: an uppercase character, a lowercase " \
                        f"character, and a digit"
        self.assertIn(
            error_message,
            self.validate("!@#$%^&*")
        )


