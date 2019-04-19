"""
forms.py - provide validation of a forms.
"""

from logging import getLogger, debug, error

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.forms import CharField, Form, PasswordInput, ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

from fpiweb.models import Box, BoxType, Constraints, Product, ProductCategory



__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"
# "${CopyRight.py}"


month_choices = [('--', '--')] + [(str(i), str(i)) for i in range(1, 13)]

def expire_year_choices():
    current_year = timezone.now().year
    years_ahead = 5
    for i in range(years_ahead + 1):
        value = str(current_year + i)
        yield value, value





# log = getLogger(__name__)


class LogoutForm(Form):
    username = CharField(
        label='Username',
        max_length=100,
    )


class LoginForm(Form):
    username = CharField(label='Username', max_length=100, )

    password = CharField(label='Password', max_length=100,
        widget=PasswordInput)


class ConstraintsForm(forms.ModelForm):
    """
    Manage Constraint details with a generic form.
    """

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = Constraints
        fields = ['id', 'constraint_name', 'constraint_descr',
                  'constraint_type', 'constraint_min', 'constraint_max',
                  'constraint_list']


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = [
            'box_number', 'box_type',
            'loc_row', 'loc_bin', 'loc_tier',
            'product',
        ]

    exp_year = forms.TypedChoiceField(
        choices=expire_year_choices,
        coerce=int,
        help_text=Box.exp_year_help_text,
    )

    exp_month_start = forms.TypedChoiceField(
        choices=month_choices,
        coerce=int,
        help_text=Box.exp_month_start_help_text,
    )

    exp_month_end = forms.TypedChoiceField(
        choices=month_choices,
        coerce=int,
        help_text=Box.exp_month_end_help_text,
    )

# EOF
