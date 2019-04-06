"""
forms.py - provide validation of a forms.
"""

from logging import getLogger, debug, error

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.forms import CharField, Form, PasswordInput, ValidationError
from django.shortcuts import get_object_or_404

from fpiweb.models import Box, BoxType, Constraints, Product, ProductCategory
__author__ = 'Travis Risner'
__project__ = "WordTrekSolver"
__creation_date__ = "04/01/2019"
# "${CopyRight.py}"

# log = getLogger(__name__)


class LoginForm(Form):
    username = CharField(
        label='Username',
        max_length=100,
    )

    password = CharField(
        label='Password',
        max_length=100,
        widget=PasswordInput
    )


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
        fields = ['constraint_id', 'constraint_name', 'constraint_descr',
                  'constraint_type', 'constraint_min', 'constraint_max',
                  'constraint_list']

# EOF
