
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "06/03/2019"

from django.db.models import Count
from django.test import TestCase

from fpiweb.forms import \
    BoxItemForm, \
    BuildPalletForm, \
    ConfirmMergeForm, \
    ExistingLocationForm, \
    ExistingLocationWithBoxesForm, \
    LocationForm, \
    MoveToLocationForm, \
    NewBoxForm
from fpiweb.models import \
    Box, \
    BoxNumber, \
    BoxType, \
    Location, \
    LocBin, \
    LocRow, \
    LocTier, \
    Product


class NewBoxFormTest(TestCase):
    """
    Test creating a new box number not previously in inventory.
    """

    fixtures = ('BoxType', 'Constraints')

    def test_save(self):
        """
        Test saving a new box number.

        :return:
        """

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
    """
    Test the form for building a pallet of boxes.
    """

    def test_is_valid__location_not_specified(self):
        form = BuildPalletForm()
        self.assertFalse(form.is_valid())


class BoxItemFormTest(TestCase):
    """
    Test adding boxes to the pallet form.
    """

    fixtures = ('BoxType', 'Product', 'ProductCategory', 'Constraints')

    def test_box_number_validation(self):
        box_number = 'blerg123'
        post_data = {
            'box_number': box_number,
            'product': Product.objects.first().pk,
            'exp_year': 2022,
        }

        form = BoxItemForm(post_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            f'{box_number} is not a valid Box Number',
            form.errors.get('box_number'),
        )

    def test_expire_months(self):
        """
        Ensure that start month <= end month
        """
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
            form.non_field_errors(),
        )


class LocationFormTest(TestCase):

    fixtures = ('LocRow', 'LocBin', 'LocTier')

    def test_is_valid__missing_value(self):

        row = LocRow.objects.get(pk=1)

        form = LocationForm({
            'loc_row': row.id,
            'loc_tier': 99,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            {'loc_bin', 'loc_tier'},
            form.errors.keys(),
        )
        self.assertEqual(
            ['This field is required.'],
            form.errors['loc_bin'],
        )
        self.assertEqual(
            ['Select a valid choice. That choice is not one of the available choices.'],
            form.errors['loc_tier'],
        )


class ExistingLocationFormTest(TestCase):

    fixtures = ('LocRow', 'LocBin', 'LocTier', 'Location')

    def test_clean__nonexistent_location(self):

        loc_row = LocRow.objects.get(loc_row='04')
        loc_bin = LocBin.objects.get(loc_bin='03')
        loc_tier = LocTier.objects.get(loc_tier='B2')

        # ----------------------
        # Non-existent location
        # ----------------------
        location = Location.get_location(loc_row, loc_bin, loc_tier)
        location.delete()

        form = ExistingLocationForm({
            'loc_row': loc_row.pk,
            'loc_bin': loc_bin.pk,
            'loc_tier': loc_tier.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            {
                '__all__': ['Location 04, 03, B2 does not exist.']
            },
            form.errors,
        )
        self.assertEqual(
            ['Location 04, 03, B2 does not exist.'],
            form.non_field_errors(),
        )

    def test_clean__multiple_locations_found(self):

        # -------------------------
        # Multiple locations found
        # -------------------------
        location = Location.get_location('04', '04', 'B1')

        # Create a duplicate location
        Location.objects.create(
            loc_row=location.loc_row,
            loc_bin=location.loc_bin,
            loc_tier=location.loc_tier
        )

        form = ExistingLocationForm({
            'loc_row': location.loc_row.pk,
            'loc_bin': location.loc_bin.pk,
            'loc_tier': location.loc_tier.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            {
                '__all__': ['Multiple 04, 04, B1 locations found'],
            },
            form.errors,
        )
        self.assertEqual(
            ['Multiple 04, 04, B1 locations found'],
            form.non_field_errors(),
        )

    def test_clean__successful_run(self):

        location = Location.get_location('04', '02', 'B1')

        form = ExistingLocationForm({
            'loc_row': location.loc_row.pk,
            'loc_bin': location.loc_bin.pk,
            'loc_tier': location.loc_tier.pk,
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(location.pk, form.cleaned_data['location'].pk)


class ExistingLocationWithBoxesFormTest(TestCase):

    fixtures = ('BoxType', 'LocRow', 'LocBin', 'LocTier', 'Location')

    def test_clean(self):

        # ----------------------------------------------------------------
        # super class's clean detects error (i.e. location doesn't exist)
        # ----------------------------------------------------------------
        loc_row = '03'
        loc_bin = '03'
        loc_tier = 'A1'

        location = Location.get_location(loc_row, loc_bin, loc_tier)
        location.delete()

        form = ExistingLocationWithBoxesForm({
            'loc_row': location.loc_row,
            'loc_bin': location.loc_bin,
            'loc_tier': location.loc_tier
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            {'__all__': ['Location 03, 03, A1 does not exist.']},
            form.errors,
        )
        self.assertEqual(
            ['Location 03, 03, A1 does not exist.'],
            form.non_field_errors(),
        )

        # ---------------------------
        # Try a location w/out boxes
        # ---------------------------

        location = Location.objects.annotate(
            box_count=Count('box')
        ).filter(
            box_count=0
        ).first()

        form = ExistingLocationWithBoxesForm({
            'loc_row': location.loc_row,
            'loc_bin': location.loc_bin,
            'loc_tier': location.loc_tier,
        })

        self.assertFalse(form.is_valid())
        expected_error = "Location {}, {}, {} doesn't have any boxes".format(
            location.loc_row.loc_row,
            location.loc_bin.loc_bin,
            location.loc_tier.loc_tier,
        )
        self.assertEqual(
            {'__all__': [expected_error]},
            form.errors,
        )
        self.assertEqual(
            [expected_error],
            form.non_field_errors(),
        )

        # ---------------------------------------------
        # Add a box to the location form will validate
        # ---------------------------------------------

        Box.objects.create(
            box_type=Box.box_type_default(),
            box_number=BoxNumber.format_box_number(111),
            location=location,
        )

        form = ExistingLocationWithBoxesForm({
            'loc_row': location.loc_row,
            'loc_bin': location.loc_bin,
            'loc_tier': location.loc_tier,
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(
            location,
            form.cleaned_data['location'],
        )


class MoveToLocationFormTest(TestCase):

    fixtures = (
        'Location',
        'LocBin',
        'LocRow',
        'LocTier',
    )

    def test_is_valid(self):
        """
        MoveToLocationForm adds the from_location field to the
        ExistingLocationForm so we only look at how from_location
        effects validation.
        :return: None
        """

        to_location = Location.get_location('01', '01', 'A2')

        form = MoveToLocationForm({
            'loc_row': to_location.loc_row,
            'loc_bin': to_location.loc_bin,
            'loc_tier': to_location.loc_tier,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            {'from_location': ['This field is required.']},
            form.errors,
        )
        self.assertEqual(
            [],
            form.non_field_errors(),
        )

        from_location = Location.get_location('01', '01', 'A1')
        form = MoveToLocationForm({
            'loc_row': to_location.loc_row,
            'loc_bin': to_location.loc_bin,
            'loc_tier': to_location.loc_tier,
            'from_location': from_location,
        })
        self.assertTrue(form.is_valid())


class ConfirmMergeFormTest(TestCase):

    fixtures = ('Location', 'LocBin', 'LocRow', 'LocTier')

    def test_is_valid(self):

        form = ConfirmMergeForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            {
                'from_location': ['This field is required.'],
                'to_location': ['This field is required.'],
                'action': ['This field is required.'],
            },
            form.errors
        )
        self.assertEqual(
            [],
            form.non_field_errors(),
        )

        from_location = Location.get_location('01', '01', 'C1')
        to_location = Location.get_location('02', '02', 'C1')

        form = ConfirmMergeForm({
            'from_location': from_location,
            'to_location': to_location,
            'action': ConfirmMergeForm.ACTION_MERGE_PALLETS,
        })
        self.assertTrue(form.is_valid(), dict(form.errors))
        self.assertEqual({}, form.errors)
        self.assertEqual([], form.non_field_errors())

    def test_boxes_at_location_int(self):
        boxes_at_to_location = 5
        form = ConfirmMergeForm(
            initial={'boxes_at_to_location': boxes_at_to_location}
        )
        self.assertEqual(
            boxes_at_to_location,
            form.boxes_at_to_location_int()
        )

    def test_to_location_str(self):
        form = ConfirmMergeForm({})
        self.assertEqual(
            'to_location not found in initial',
            form.to_location_str(),
        )

        to_location = Location.get_location('02', '02', 'C1')
        form = ConfirmMergeForm(
            initial={
                'to_location': to_location,
            }
        )
        self.assertEqual('02, 02, C1', form.to_location_str())








