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
    ModelChoiceField, \
    PasswordInput, \
    ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

from fpiweb.models import \
    Box, \
    BoxNumber, \
    BoxType, \
    Constraints, \
    Location, \
    LocRow, \
    LocBin, \
    LocTier, \
    Pallet, \
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


def validate_exp_month_start_end(exp_month_start, exp_month_end):
    """
    Validate the start and end month, if given.

    :param exp_month_start: number 1-12 (integer or string)
    :param exp_month_end: number 1-12 (integer or string)
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

    try:
        exp_month_start = int(exp_month_start)
    except (TypeError, ValueError):
        raise ValidationError(
            "Exp month start {} is not an integer".format(
                repr(exp_month_start),
            )
        )

    try:
        exp_month_end = int(exp_month_end)
    except (TypeError, ValueError):
        raise ValidationError(
            "Exp month end {} is not an integer".format(
                repr(exp_month_end)
            )
        )

    if exp_month_end <= exp_month_start:
        raise ValidationError(
            'Exp month end must be after Exp month start'
        )


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


class LocRowForm(forms.ModelForm):
    """
    Manage Loction row details with a generic form.
    """

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = LocRow
        fields = ['id', 'loc_row', 'loc_row_descr', ]

    loc_row = forms.CharField(
        help_text=LocRow.loc_row_help_text,
        required=True,
    )

    @staticmethod
    def validate_loc_row_fields(
            loc_row_name: str,
            loc_row_descr: str,
    ):
        """
        Validate the various location row record fields.

        :param loc_row_name: name of row
        :param loc_row_descr: description of row
        :return: True if valid
        """
        max_len: int = LocRow.loc_row_max_length
        min_len: int = LocRow.loc_row_min_length
        if not loc_row_name or not (len(loc_row_name) > 0):
            raise ValidationError(
                'The row must be specified'
            )
        if (len(loc_row_name) <= max_len) \
                and \
                (len(loc_row_name) >= min_len) \
                and \
                (loc_row_name.isdigit()):
            ...
        else:
            raise ValidationError(
                'A row must be two digits (with a leading zero if needed)'
            )
        if not loc_row_descr or not (len(loc_row_descr) > 0):
            raise ValidationError(
                'A description of this row must be provided'
            )

        return

    def clean(self):
        """
        Clean and validate the data given for the constraint record.

        :return:
        """
        cleaned_data = super().clean()
        loc_row_name = cleaned_data.get('loc_row')
        loc_row_descr = cleaned_data.get('loc_row_descr')
        self.validate_loc_row_fields(loc_row_name, loc_row_descr)
        return


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
        # valid: bool = False
        if not loc_bin_name or not (len(loc_bin_name) > 0):
            raise ValidationError(
                'The bin must be specified'
            )
        if (len(loc_bin_name) <= max_len) \
                and \
                (len(loc_bin_name) >= min_len) \
                and \
                (loc_bin_name.isdigit()):
            ...
        else:
            raise ValidationError(
                'A bin must be two digits (with a leading zero if needed)'
            )
        if not loc_bin_descr or not (len(loc_bin_descr) > 0):
            raise ValidationError(
                'A description of this bin must be provided'
            )
        return


    def clean(self):
        """
        Clean and validate the data given for the bin record.

        :return:
        """
        cleaned_data = super().clean()
        loc_bin_name = cleaned_data.get('loc_bin')
        loc_bin_descr = cleaned_data.get('loc_bin_descr')
        self.validate_loc_bin_fields(loc_bin_name, loc_bin_descr)
        return


class LocTierForm(forms.ModelForm):
    """
    Manage Loction tier details with a generic form.
    """

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = LocTier
        fields = ['id', 'loc_tier', 'loc_tier_descr', ]

    loc_tier = forms.CharField(
        help_text=LocTier.loc_tier_help_text,
        required=True,
    )

    @staticmethod
    def validate_loc_tier_fields(
            loc_tier_name: str,
            loc_tier_descr: str,
    ):
        """
        Validate the various location tier record fields.

        :param loc_tier_name: name of tier
        :param loc_tier_descr: description of tier
        :return: True if valid
        """
        max_len: int = LocTier.loc_tier_max_length
        min_len: int = LocTier.loc_tier_min_length
        if not loc_tier_name or not (len(loc_tier_name) > 0):
            raise ValidationError(
                'The tier must be specified'
            )
        if (len(loc_tier_name) <= max_len) \
                and \
                (len(loc_tier_name) >= min_len) \
                and \
                (loc_tier_name[0].isalpha())\
                and \
                (loc_tier_name[1].isdigit())\
                :
            ...
        else:
            raise ValidationError(
                'A tier must be a character followed by a digit'
            )
        if not loc_tier_descr or not (len(loc_tier_descr) > 0):
            raise ValidationError(
                'A description of this tier must be provided'
            )
        return

    def clean(self):
        """
        Clean and validate the data given for the tier record.

        :return:
        """
        cleaned_data = super().clean()
        loc_tier_name = cleaned_data.get('loc_tier')
        loc_tier_descr = cleaned_data.get('loc_tier_descr')
        self.validate_loc_tier_fields(loc_tier_name, loc_tier_descr)
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
            con_name: str,
            con_descr: str,
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
        if not con_name or not (len(con_name) > 0):
            raise ValidationError('Constraint name must be specified')
        if not con_descr or not (len(con_descr) > 0):
            raise ValidationError(
                'A description of this constraint must be provided'
            )
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
        con_descr = cleaned_data.get('constraint_descr')
        con_type = cleaned_data.get('constraint_type')
        con_min = cleaned_data.get('constraint_min')
        con_max = cleaned_data.get('constraint_max')
        con_list = cleaned_data.get('constraint_list')
        self.validate_constraint_fields(
            con_name,
            con_descr,
            con_type,
            con_min,
            con_max,
            con_list
        )
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
        # widgets = {
        #     'date_filled': Html5DateInput
        # }

    # product = forms.ModelChoiceField(
    #
    # )

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

    def clean(self):
        """
        Clean and validate the data in this box record.

        :return:
        """
        cleaned_data = super().clean()
        exp_month_start = cleaned_data.get('exp_month_start')
        exp_month_end = cleaned_data.get('exp_month_end')
        self.validate_exp_month_start_end(exp_month_start, exp_month_end)


# class BuildPalletForm(forms.Form):
#     # Don't try and turn this into a Model Form.  We're performing a search,
#     # not creating a new Location or editing an existing one.
#
#     loc_row = forms.ModelChoiceField(
#         LocRow.objects.all(),
#         required=True,
#     )
#
#     loc_bin = forms.ModelChoiceField(
#         LocBin.objects.all(),
#         required=True,
#     )
#
#     loc_tier = forms.ModelChoiceField(
#         LocTier.objects.all(),
#         required=True,
#     )


class BuildPalletForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            'loc_row',
            'loc_bin',
            'loc_tier',
        )

    def clean(self):
        cleaned_data = super().clean()

        # The values returned are LocRow, LocBin, and LocTier objects
        loc_row = cleaned_data['loc_row']
        loc_bin = cleaned_data['loc_bin']
        loc_tier = cleaned_data['loc_tier']

        try:
            self.instance = Location.objects.get(
                loc_row=loc_row,
                loc_bin=loc_bin,
                loc_tier=loc_tier,
            )
        except Location.DoesNotExist:
            raise forms.ValidationError(
                "Location row={} bin={} tier={} not found.".format(
                    loc_row.loc_row,
                    loc_bin.loc_bin,
                    loc_tier.loc_tier,
                )
            )

        return cleaned_data


class BoxItemForm(forms.Form):
    """Form for the Box as it appears as part of a formset on the Build Pallet
    page"""

    # I've deliberately removed the ID field so that this form may
    # be used for either Box or PalletBox records.

    # This is a read only field.  In the page a box number is displayed in an input element with no name or id
    box_number = forms.CharField(
        max_length=Box.box_number_max_length,
        min_length=Box.box_number_min_length,
        widget=forms.HiddenInput,
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

    exp_month_start = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=12,
    )

    exp_month_end = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=12,
    )

    # clean method copied from FillBoxForm
    def clean(self):
        cleaned_data = super().clean()
        exp_month_start = cleaned_data.get('exp_month_start')
        exp_month_end = cleaned_data.get('exp_month_end')
        validate_exp_month_start_end(exp_month_start, exp_month_end)
        return cleaned_data

    @staticmethod
    def get_initial_from_box(box):
        """
        :param box: Box or PalletBox record
        :return: 
        """
        return {
            'box_number': box.box_number,
        }




class PrintLabelsForm(forms.Form):

    starting_number = forms.IntegerField()

    number_to_print = forms.IntegerField(
        initial=10,
    )


class LocationForm(forms.ModelForm):
    """A form for use whenever you need to select row, bin, and tier"""
    class Meta:
        model = Location
        fields = (
            'loc_row',
            'loc_bin',
            'loc_tier',
        )


class ExistingLocationForm(LocationForm):

    def clean(self):
        cleaned_data = super().clean()

        loc_row = cleaned_data.get('loc_row')
        loc_bin = cleaned_data.get('loc_bin')
        loc_tier = cleaned_data.get('loc_tier')

        try:
            location = Location.objects.get(
                loc_row=loc_row,
                loc_bin=loc_bin,
                loc_tier=loc_tier,
            )
        except Location.DoesNotExist:
            raise ValidationError(
                f"Location {loc_bin.loc_bin}, {loc_row.loc_row}, {loc_tier.loc_tier} does not exist."
            )
        except Location.MultipleObjectsReturned:
            raise ValidationError(
                r"Multiple {loc_bin.loc_bin}, {loc_row.loc_row}, {loc_tier.loc_tier} locations found"
            )

        cleaned_data['location'] = location
        return cleaned_data


class BoxNumberField(forms.CharField):
    """Accepts box number with or without BOX prefix.
    Returns BoxNumber with BOX prefix and leading zeros"""

    def clean(self, value):
        value = super().clean(value)

        if BoxNumber.validate(value):
            return value.upper()

        # Did the user just enter digit?  Try and turn this
        # into a valid bo number
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValidationError(
                '%(value)s is not a valid box number',
                params={'value': value},
            )

        return BoxNumber.format_box_number(value)


class ExtantBoxNumberField(BoxNumberField):
    """Checks whether there's a Box with the specified box number in the
    database.  If a matching Box is found, this Box is stored in the
    field's box attribute"""

    def clean(self, value):
        value = super().clean(value)
        if not Box.objects.filter(box_number=value).exists():
            raise ValidationError(
                "Box number %(value)s is not present in the database.",
                params={'value': value},
            )
        return value


class ExtantBoxNumberForm(forms.Form):

    box_number = ExtantBoxNumberField(
        max_length=Box.box_number_max_length,
    )


class PalletSelectForm(forms.Form):

    pallet = ModelChoiceField(
        queryset=Pallet.objects.order_by('name'),
        empty_label='Select a Pallet',
    )


class PalletNameForm(forms.ModelForm):
    class Meta:
        model = Pallet
        fields = ('name',)


class HiddenPalletForm(forms.Form):
    pallet = ModelChoiceField(
        queryset=Pallet.objects.all(),
        widget=forms.HiddenInput,
    )

# EOF
