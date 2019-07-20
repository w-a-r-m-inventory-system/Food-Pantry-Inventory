"""
forms.py - provide validation of a forms.
"""

from logging import getLogger, debug, error
from typing import Union, Optional

from django import forms
from django.forms import \
    CharField, \
    DateInput, \
    Form, \
    PasswordInput, \
    ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

from fpiweb.models import \
    Box, \
    BoxType, \
    Constraints, \
    LocRow, \
    LocBin, \
    LocTier, \
    Product, \
    ProductCategory

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"
# "${CopyRight.py}"


logger = getLogger('fpiweb')


def add_no_selection_choice(other_choices, dash_count=2):
    return [(None, '-' * dash_count)] + list(other_choices)


def month_choices():
    return add_no_selection_choice(
        [(str(i), str(i)) for i in range(1, 13)]
    )


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
    return add_no_selection_choice(min_max_choices('Row'))


def bin_choices():
    return add_no_selection_choice(min_max_choices('Bin'))


def tier_choices():
    return add_no_selection_choice(char_list_choices('Tier'))


def none_or_int(text: str) -> Optional[int]:
    """
    Convert test to a valid integer or None.

    :param text:
    :return:
    """
    if text is None or text.strip() == '':
        result = None
    elif text.isnumeric():
        result = int(text)
    else:
        result = None
    return result


def none_or_str(text: str) -> Optional[str]:
    """
    Convert text to non-empty string or None.

    :param text:
    :return:
    """
    if text is None or text.strip() == '':
        result = None
    else:
        result = text
    return result


def none_or_list(text: str) -> Optional[list]:
    """
    Convert text to list or None.

    :param text:
    :return:
    """
    if text is None or text.strip() == '':
        result = None
    else:
        valid_list = True
        result = list()
        text_parts = text.split()
        for pos, part in enumerate(text_parts):
            element = part.strip()
            if element.endswith(','):
                value = element[:-1]
            elif pos + 1 == len(text_parts):
                value = element
            else:
                valid_list = False
                break
            if not value.isalnum():
                valid_list = False
                break
            result.append(value)
        if not valid_list:
            result = None
    return result


def validate_int_list(char_list: list) -> bool:
    """
    Verify that all values in the list are integers.

    :param text:
    :return:
    """
    valid_int_list = True
    for element in char_list:
        if not element.isnumeric():
            valid_int_list = False
            break
    return valid_int_list


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


class LocBinForm(forms.ModelForm):
    """
    Manage Loction bin details with a generic form.
    """

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = LocBin
        fields = ['id', 'loc_bin', 'loc_bin_descr', ]

    loc_bin = forms.CharField(
        help_text=LocBin.loc_bin_help_text,
        required=True,
    )

    constraint_max = forms.CharField(
        help_text=LocBin.loc_bin_descr_help_text,
        required=True,
    )

    @staticmethod
    def validate_loc_bin_fields(
            loc_bin_name: str,
            loc_bin_descr: str,
    ):
        """
        Validate the various location bin record fields.

        :param loc_bin_name: name of bin
        :param loc_bin_descr: description of bin
        :return: True if valid
        """
        max_len: int = LocBin.loc_bin_max_length
        min_len: int = LocBin.loc_bin_min_length
        valid: bool = False
        if (len(loc_bin_name) <= max_len) \
                and \
                (len(loc_bin_name) >= min_len) \
                and \
                (loc_bin_name.isdigit()):
            valid = True
        if not valid:
            raise ValidationError(
                'A bin must be two digits (with a leading zero if needed)'
            )

        return


def clean(self):
    """
    Clean and validate the data given for the constraint record.

    :return:
    """
    cleaned_data = super().clean()
    loc_bin_name = cleaned_data.get('loc_bin')
    if not loc_bin_name or not (len(loc_bin_name) > 0):
        raise ValidationError(
            'The bin must be specified'
        )
    loc_bin_descr = cleaned_data.get('loc_bin_descr')
    if not loc_bin_descr or not (len(loc_bin_descr) > 0):
        raise ValidationError(
            'A description of this bin must be provided'
        )
    self.validate_loc_bin_fields(loc_bin_name, loc_bin_descr)
    return


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

    constraint_type = forms.ChoiceField(
        choices=Constraints.CONSTRAINT_TYPE_CHOICES,
        help_text=Constraints.constraint_type_help_text,
    )

    constraint_min = forms.CharField(
        required=False,
        help_text=Constraints.constraint_min_help_text,
    )

    constraint_max = forms.CharField(
        required=False,
        help_text=Constraints.constraint_max_help_text,
    )

    constraint_list = forms.CharField(
        required=False,
        help_text=Constraints.constraint_list_help_text,
    )

    @staticmethod
    def validate_constraint_fields(
            con_type: Constraints.CONSTRAINT_TYPE_CHOICES,
            con_min: Union[str, int],
            con_max: Union[str, int],
            con_list: str
    ):
        """
        Validate the various constraint record fields.

        :param con_name: name of constraint
        :param con_type: type of constraint
        :param con_min: minimum value, if given
        :param con_max: maximum value, if given
        :param con_list: list of values, if given
        :return:
        """
        max_val = none_or_str(con_max)
        min_val = none_or_str(con_min)
        list_val = none_or_list(con_list)
        valid: bool = False
        if con_type == Constraints.INT_RANGE:
            if max_val and min_val and (not list_val):
                max_int = none_or_int(max_val)
                min_int = none_or_int(min_val)
                if min_int and max_int and min_int < max_int:
                    valid = True
            if not valid:
                raise ValidationError(
                    'Integer range requires that the min and max be integers '
                    'and that max must be greater than min (and no list)'
                )
        elif con_type == Constraints.CHAR_RANGE:
            if max_val and min_val and (not list_val):
                if min_val < max_val:
                    valid = True
            if not valid:
                raise ValidationError(
                    'Character range requires that the min and max be '
                    'characters and that max must be greater than min '
                    '(and no list)'
                )
        elif con_type == Constraints.CHAR_LIST:
            if max_val or min_val or (not list_val):
                raise ValidationError(
                    'Character list requires that min and max be empty and '
                    'that the list contain only alphanumeric characters '
                    'separated with commas'
                )
        elif con_type == Constraints.INT_LIST:
            if max_val or min_val or (not list_val):
                raise ValidationError(
                    'Integer list requires that min and max be empty and '
                    'that the list contain only numbers separated with commas'
                )
        return

    def clean(self):
        """
        Clean and validate the data given for the constraint record.

        :return:
        """
        cleaned_data = super().clean()
        con_name = cleaned_data.get('constraint_name')
        if not con_name or not (len(con_name) > 0):
            raise ValidationError('Constraint name must be specified')
        con_descr = cleaned_data.get('constraint_descr')
        if not con_descr or not (len(con_descr) > 0):
            raise ValidationError(
                'A description of this constraint must be provided'
            )
        con_type = cleaned_data.get('constraint_type')
        con_min = cleaned_data.get('constraint_min')
        con_max = cleaned_data.get('constraint_max')
        con_list = cleaned_data.get('constraint_list')
        self.validate_constraint_fields(con_type, con_min, con_max, con_list)
        return


class NewBoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = [
            'box_number',
            'box_type',
        ]

    box_number = forms.CharField(
        max_length=Box.box_number_max_length,
        min_length=Box.box_number_min_length,
        required=False,
        disabled=True
    )

    def save(self, commit=True):
        if self.instance and not self.instance.pk:
            if self.instance.box_type:
                box_type = self.instance.box_type
                self.instance.quantity = box_type.box_type_qty
        return super(NewBoxForm, self).save(commit=commit)


class FillBoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = [
            'product',
            'exp_year',
            'exp_month_start',
            'exp_month_end',
            # 'date_filled',
        ]

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
        """
        Validate the start and end month, if given.

        :param exp_month_start:
        :param exp_month_end:
        :return:
        """
        if exp_month_start is None and exp_month_end is None:
            return

        error_msg = (
            "If Exp {} month is specified, Exp {} month must be specified"
        )

        if exp_month_start is not None and exp_month_end is None:
            raise ValidationError(error_msg.format('start', 'end'))

        if exp_month_end is not None and exp_month_start is None:
            raise ValidationError(error_msg.format('end', 'start'))

        if exp_month_end <= exp_month_start:
            raise ValidationError(
                'Exp month end must be after Exp month start'
            )

    def clean(self):
        """
        Clean and validate the data in this box record.

        :return:
        """
        cleaned_data = super().clean()
        exp_month_start = cleaned_data.get('exp_month_start')
        exp_month_end = cleaned_data.get('exp_month_end')
        self.validate_exp_month_start_end(exp_month_start, exp_month_end)


class MoveBoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = [
            'loc_row',
            'loc_bin',
            'loc_tier',
        ]

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


class BuildPalletForm(forms.Form):
    # This may be changed to a Model form for the Location Table

    loc_row = forms.ModelChoiceField(
        LocRow.objects.all(),
        required=True,
    )

    loc_bin = forms.ModelChoiceField(
        LocBin.objects.all(),
        required=True,
    )

    loc_tier = forms.ModelChoiceField(
        LocTier.objects.all(),
        required=True,
    )


class BoxItemForm(forms.ModelForm):
    """Form for the Box as it appears as part of a formset on the Build Pallet
    page"""

    class Meta:
        model = Box
        fields = [
            'box_id',
            'box_number',
            'product',
            'exp_year',
        ]

    box_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    box_number = forms.CharField(
        max_length=Box.box_number_max_length,
        min_length=Box.box_number_min_length,
        disabled=True,
    )

    product = forms.ModelChoiceField(
        Product.objects.all(),
        required=True,
    )

    exp_year = forms.TypedChoiceField(
        choices=expire_year_choices,
        coerce=int,
        help_text=Box.exp_year_help_text,
    )

# EOF
