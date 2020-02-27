
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "06/03/2019"

from django.test import TestCase

from fpiweb.forms import \
    BoxItemForm, \
    BuildPalletForm,\
    NewBoxForm
from fpiweb.models import \
    Box, \
    BoxNumber, \
    BoxType, \
    Product


class NewBoxFormTest(TestCase):

    fixtures = ('BoxType', 'Constraints')

    def test_save(self):

        box_type = BoxType.objects.get(box_type_code='Evans')

        post_data = {
            'box_number': '27',
            'box_type': box_type.pk,
        }

        form = NewBoxForm(post_data)
        self.assertTrue(
            form.is_valid(),
            f"{form.errors} {form.non_field_errors()}",
        )
        form.save(commit=True)

        box = form.instance
        self.assertIsNotNone(box)
        self.assertIsNotNone(box.pk)
        self.assertEqual(box_type.box_type_qty, box.quantity)


class BuildPalletFormTest(TestCase):

    def test_is_valid__location_not_specified(self):
        form = BuildPalletForm()
        self.assertFalse(form.is_valid())


class BoxItemFormTest(TestCase):

    fixtures = ('BoxType', 'Product', 'ProductCategory', 'Constraints')

    def test_expire_months(self):
        """ensure that start month <= end month"""
        post_data = {
            'box_number': BoxNumber.format_box_number(12),
            'product': Product.objects.first().pk,
            'exp_year': 2022,
            'exp_month_start': 5,
            'exp_month_end': 3,
        }

        form = BoxItemForm(post_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Exp month end must be later than or equal to Exp month start',
            form.non_field_errors()
        )

