"""
test_support_activity.py - Test handling activity records.
"""

from logging import getLogger, debug, error

from django.test import TestCase

from fpiweb.models import Box, Pallet, PalletBox, Activity, LocRow, LocBin, \
    LocTier, Location, BoxType, Product, ProductCategory
from fpiweb.support.BoxActivity import BoxActivityClass

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "08/19/2019"


# "${Copyright.py}"


class test_support_activityClass(TestCase):
    """
    test_support_activityClass - Test handling activity records.
    """
    # identify and load data for these tests
    fixtures = [
        'Box', 'Pallet', 'PalletBox',  'BoxType', 'Product', 'ProductCategory',
        'LocRow', 'LocBin', 'LocTier', 'Location',
        'User', 'Profile', 'UserGroups', 'Group',
    ]

    @classmethod
    def setUpClass(cls) -> None:
        """
        Prepare to test activity creation and manipulation.

        :return:
        """
        super().setUpClass()
        return

    def test_box_add_activity(self) -> None:
        """
        Test adding a box under various circumstances.

        :return:
        """
        full_box = Box.objects.select_related(
            'product', 'product__prod_cat', 'box_type',
        ).get(box_number='BOX12345')
        ba = BoxActivityClass()
        ba.box_add(full_box.id)
        full_activity = Activity.objects.get(
            box_number=full_box.box_number, date_filled=full_box.date_filled
        )
        assert full_activity.box_type == full_box.box_type.box_type_code
        assert full_activity.loc_row == full_box.loc_row
        assert full_activity.loc_bin == full_box.loc_bin
        assert full_activity.loc_tier == full_box.loc_tier
        assert full_activity.prod_name == full_box.product.prod_name
        assert full_activity.prod_cat_name == \
               full_box.product.prod_cat.prod_cat_name
        assert full_activity.date_consumed == None
        assert full_activity.exp_year == full_box.exp_year
        assert full_activity.exp_month_start == full_box.exp_month_start
        assert full_activity.exp_month_end == full_box.exp_month_end
        assert full_activity.quantity == full_box.box_type.box_type_qty
        assert full_activity.duration == 0
        assert full_activity.adjustment_code == None
        return

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Testing done, discard testing data.
        :return:
        """
        super().tearDownClass()
        return

# EOF
