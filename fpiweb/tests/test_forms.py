
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "06/03/2019"

from django.test import TestCase

from fpiweb.forms import BoxForm
from fpiweb.models import Box, BoxType


class BoxFormTest(TestCase):

    fixtures = ('BoxType', 'Constraints')

    def test_save(self):

        box_type = BoxType.objects.get(box_type_code='Evans')

        post_data = {
            'box_number': '27',
            'box_type': box_type.pk,
            'loc_row': '1',
            'loc_bin': '1',
            'loc_tier': 'A1',
            'exp_year': '2019',
        }

        form = BoxForm(post_data)
        self.assertTrue(
            form.is_valid(),
            f"{form.errors} {form.non_field_errors()}",
        )
        form.save(commit=True)

        box = form.instance
        self.assertIsNotNone(box)
        self.assertIsNotNone(box.pk)
        self.assertEqual(box_type.box_type_qty, box.quantity)







