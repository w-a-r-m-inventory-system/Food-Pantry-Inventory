"""
test_support_activity.py - Test handling activity records.
"""
from datetime import datetime, timezone, timedelta
from logging import getLogger, debug, error

from django.test import TestCase, TransactionTestCase
from django.utils.timezone import now

from FPIDjango.settings import TIME_ZONE
from fpiweb.models import \
    Box, \
    Activity, \
    LocRow, \
    LocBin, \
    LocTier, \
    Location, \
    BoxType, \
    Product, \
    ProductCategory
from fpiweb.support.BoxActivity import BoxActivityClass

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "08/19/2019"


# "${Copyright.py}"


class ActivitySupportTestCase(TransactionTestCase):
    """
    test_support_activityClass - Test handling activity records.
    """
    # identify and load data for these tests
    fixtures = [
        'Box', 'BoxType', 'Product', 'ProductCategory',
        'LocRow', 'LocBin', 'LocTier', 'Location', 'Activity'
    ]

    # 'User', 'UserGroups', 'Group', 'Profile',

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
            box_number__exact=full_box.box_number,
            date_filled__exact=full_box.date_filled
        )
        assert full_activity.box_type == full_box.box_type.box_type_code
        assert full_activity.loc_row == full_box.loc_row
        assert full_activity.loc_bin == full_box.loc_bin
        assert full_activity.loc_tier == full_box.loc_tier
        assert full_activity.prod_name == full_box.product.prod_name
        assert full_activity.prod_cat_name == \
               full_box.product.prod_cat.prod_cat_name
        assert full_activity.date_consumed is None
        assert full_activity.exp_year == full_box.exp_year
        assert full_activity.exp_month_start == full_box.exp_month_start
        assert full_activity.exp_month_end == full_box.exp_month_end
        assert full_activity.quantity == full_box.box_type.box_type_qty
        assert full_activity.duration == 0
        assert full_activity.adjustment_code is None
        return

    def test_box_move(self) -> None:
        """
        Test moving a box under various circumstances.

        :return:
        """
        # get a box at a known location
        full_box = Box.objects.get(box_number='BOX12346')

        # get a new location with related records
        location = Location.objects.select_related(
            'loc_row', 'loc_bin', 'loc_tier'
        ).get(loc_code='0409C2')

        # move the box to a new location and save changes
        full_box.loc_row = location.loc_row.loc_row
        full_box.loc_bin = location.loc_bin.loc_bin
        full_box.loc_tier = location.loc_tier.loc_tier
        full_box.save()

        # modify the activity record to match
        ba = BoxActivityClass()
        ba.box_move(full_box.id)
        full_activity = Activity.objects.get(
            box_number=full_box.box_number,
            date_filled=full_box.date_filled
        )
        assert full_activity.box_type == full_box.box_type.box_type_code
        assert full_activity.loc_row == full_box.loc_row
        assert full_activity.loc_bin == full_box.loc_bin
        assert full_activity.loc_tier == full_box.loc_tier
        assert full_activity.prod_name == full_box.product.prod_name
        assert full_activity.prod_cat_name == \
               full_box.product.prod_cat.prod_cat_name
        assert full_activity.date_consumed is None
        assert full_activity.exp_year == full_box.exp_year
        assert full_activity.exp_month_start == full_box.exp_month_start
        assert full_activity.exp_month_end == full_box.exp_month_end
        assert full_activity.quantity == full_box.box_type.box_type_qty
        assert full_activity.duration == 0
        assert full_activity.adjustment_code is None
        return

    def text_box_consume(self) -> None:
        """
        Test consuming a box under various circumstances.

        :return:
        """
        # get a box to consume
        empty_box = Box.objects.select_related(
            'box_type').get(box_number='BOX12355')

        # consume it and save changes
        empty_box.loc_row = None
        empty_box.loc_bin = None
        empty_box.loc_tier = None
        empty_box.product = None
        empty_box.exp_year = None
        empty_box.exp_month_start = None
        empty_box.exp_month_end = None
        empty_box.date_filled = None
        empty_box.save()

        # modify the activity record to match
        ba = BoxActivityClass()
        ba.box_empty(empty_box.id)
        activity_set = Activity.objects.filter(
            box_number__exact=empty_box.box_number).order_by(
            'date_filled'
        )
        assert len(activity_set) > 0
        empty_activity = activity_set[0]
        assert empty_activity.date_filled is not None
        assert empty_activity.date_filled < datetime.now(tz=TIME_ZONE)
        assert empty_activity.date_consumed is not None
        min_time_diff = timedelta(seconds=60)
        min_time = now() - min_time_diff
        assert empty_activity.date_consumed > min_time
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
