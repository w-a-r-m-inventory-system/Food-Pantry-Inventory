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


class ConstraintsForm(forms.ModelForm):
    """
    Manage Constraint details with a generic form.
    """

    class Meta:
        """
        Additional info to help Django provide intelligent defaults.
        """
        model = Constraints
        fields = ['ConstraintID', 'ConstraintName', 'ConstraintDescr',
                  'ConstraintType', 'ConstraintMin', 'ConstraintMax',
                  'ConstraintList']

    def clean(self):
        """
        Additional form validation logic.

        **Important Note:**
        Currently a new animal does not go through this method for
        validation.  If I ever figure out why, I will implement the new
        portion of the comments below.

        :return:
        """

        # items not yet validated:
        # - animal:
        #   - name is not (case insensitive) "Daily Quest"
        #   - new:
        #     - name is unique amongst animals
        #     - order is unique amonst animals
        # - daily quest:
        #   - name = 'Daily Quest'
        #   - order = 1
        #   - date-started is unique

        # determine if new or edit
        # TODO Determine how to validate new entries - 1/19/17

        # # animal validation
        #
        # # get the id of the existing record
        # animal_id = self.instance.id
        #
        # # find out if it is now an animal or a daily quest
        # category = self.cleaned_data.get('category')
        #
        # # retrieve other cleaned data for our use
        # order = self.cleaned_data.get('animal_order')
        # name = self.cleaned_data.get('animal_name')
        # date_started = self.cleaned_data.get('date_started')

        # # daily quest validation
        # if category == Constraints.DAILY_QUEST_IND:
        #     if order != 1:
        #         raise ValidationError('The order for daily quests must be 1.')
        #     if name != 'Daily Quest':
        #         raise ValidationError('The name must be "Daily Quest" for '
        #                               'daily quests.')
        #     dq_set_same_date = Constraints.objects.filter(
        #         date_started__exact=date_started).exclude(
        #         id__exact=animal_id).exclude(category__exact='D')
        #     if len(dq_set_same_date) > 0:
        #         raise ValidationError(
        #             'The date started for daily quests must be unique.'
        #         )

        # # Other category validation
        # elif category == Constraints.OTHER_IND:
        #     if order != 1:
        #         raise ValidationError('The order for other categories must be '
        #                               '1.')
        #     if name.casefold() == 'daily quest':
        #         raise ValidationError('The name must not be "Daily Quest" for '
        #                               'other category.')
        #     dq_set_same_date = Constraints.objects.filter(
        #         date_started__exact=date_started).exclude(
        #         id__exact=animal_id).exclude(category__exact='Z')
        #     if len(dq_set_same_date) > 0:
        #         raise ValidationError(
        #             'The date started for other quests must be unique.'
        #         )

        # # animal validation
        # elif category == Constraints.ANIMAL_IND:
        #     # check animal order
        #     animal_set_order = Constraints.objects.filter(
        #         animal_order__exact=order).exclude(
        #         id__exact=animal_id).exclude(category__exact='D')
        #     if len(animal_set_order) > 0:
        #         raise ValidationError(
        #             'The order for animals must be unique.'
        #         )
        #
        #     # check animal name
        #     if name.casefold() == 'daily quest':
        #         raise ValidationError('Constraints name cannot be "Daily Quest')
        #     animal_set_name = Constraints.objects.filter(
        #         animal_name__exact=name).exclude(id__exact=animal_id)
        #     if len(animal_set_name) > 0:
        #         raise ValidationError('The name of the animal must be unique.')


        return self.cleaned_data



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

# EOF
