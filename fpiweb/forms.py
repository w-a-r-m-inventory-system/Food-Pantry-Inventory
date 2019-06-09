"""
forms.py - provide validation of a forms.
"""

from logging import getLogger, debug, error

from django import forms
from django.forms import CharField, DateInput, Form, PasswordInput, ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

from fpiweb.models import Box, BoxType, Constraints, Product, ProductCategory


__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"
# "${CopyRight.py}"


month_choices = [(None, '--')] + [(str(i), str(i)) for i in range(1, 13)]

logger = getLogger('fpiweb')


def expire_year_choices():
    current_year = timezone.now().year
    years_ahead = 5
    for i in range(years_ahead + 1):
        value = str(current_year + i)
        yield value, value


def min_max_choices(constraint_name):
    min_value, max_value = Constraints.get_values(constraint_name)
    select_range = [str(i) for i in range(min_value, max_value + 1)]
    return list(zip(select_range, select_range))


def char_list_choices(constraint_name):
    values = Constraints.get_values(constraint_name)
    return list(zip(values, values))


def row_choices():
    return min_max_choices('Row')


def bin_choices():
    return min_max_choices('Bin')


def tier_choices():
    return char_list_choices('Tier')


def none_or_int(text):
    if text is None or text.strip() == '':
        return None
    return int(text)


class Html5DateInput(DateInput):
    input_type = 'date'


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
            'box_number',
            'box_type',
            'loc_row',
            'loc_bin',
            'loc_tier',
            'product',
            'exp_year',
            'exp_month_start',
            'exp_month_end',
            'date_filled',
        ]
        widgets = {
            'date_filled': Html5DateInput
        }

    loc_row = forms.ChoiceField(
        choices=row_choices,
        help_text=Box.loc_row_help_text,
    )

    loc_bin = forms.ChoiceField(
        choices=bin_choices,
        help_text=Box.loc_bin_help_text,
    )

    loc_tier = forms.ChoiceField(
        choices=tier_choices,
        help_text=Box.loc_tier_help_text,
    )

    exp_year = forms.TypedChoiceField(
        choices=expire_year_choices,
        coerce=int,
        help_text=Box.exp_year_help_text,
    )

    exp_month_start = forms.TypedChoiceField(
        choices=month_choices,
        required=False,
        empty_value=None,
        coerce=none_or_int,
        help_text=Box.exp_month_start_help_text,
    )

    exp_month_end = forms.TypedChoiceField(
        choices=month_choices,
        required=False,
        empty_value=None,
        coerce=none_or_int,
        help_text=Box.exp_month_end_help_text,
    )

    @staticmethod
    def validate_exp_month_start_end(exp_month_start, exp_month_end):
        if exp_month_start is None and exp_month_end is None:
            return

        error_msg = "If Exp {} month is specified, Exp {} month must be specified"

        if exp_month_start is not None and exp_month_end is None:
            raise ValidationError(error_msg.format('start', 'end'))

        if exp_month_end is not None and exp_month_start is None:
            raise ValidationError(error_msg.format('end', 'start'))

        if exp_month_end <= exp_month_start:
            raise ValidationError('Exp month end must be after Exp month start')

    def clean(self):
        cleaned_data = super().clean()
        exp_month_start = cleaned_data.get('exp_month_start')
        exp_month_end = cleaned_data.get('exp_month_end')
        self.validate_exp_month_start_end(exp_month_start, exp_month_end)

    def save(self, commit=True):
        if self.instance and not self.instance.pk:
            if self.instance.box_type:
                box_type = self.instance.box_type
                self.instance.quantity = box_type.box_type_qty
        super(BoxForm, self).save(commit=commit)




# EOF
