"""
test_support_box_and_activity.py - Test handling activity records.
"""
from typing import NamedTuple

from django.test import TransactionTestCase
from django.utils.timezone import now
from pytest import raises

from fpiweb.constants import InvalidActionAttemptedError, InvalidValueError
from fpiweb.models import Box, Activity, Location, BoxType, Product, Pallet, \
    BoxNumber, PalletBox
from fpiweb.support.BoxManagement import BoxManagementClass

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "08/19/2019"


# "${Copyright.py}"

class PalletBoxInfo(NamedTuple):
    """
    Holds an entry in the dictionary of pallet box info.
    """
    pallet_box_id: int
    box_id: int
    box_number: str
    product: str
    exp_year: int


class BoxSupportTestCase(TransactionTestCase):
    """
    test_support_activityClass - Test handling activity records.
    """
    # identify and load data for these tests
    fixtures = [
        'Box',
        'BoxType',
        'Product',
        'ProductCategory',
        'LocRow',
        'LocBin',
        'LocTier',
        'Location',
        'Activity',
        'Constraints',
    ]

    # 'User', 'UserGroups', 'Group', 'Profile',

    @classmethod
    def setUpClass(cls) -> None:
        """
        Prepare to test box creation and manipulation.

        :return:
        """
        super().setUpClass()
        # add any additional setup needed here
        return

    def test_box_new(self) -> None:
        """
        Test adding a new box number to the inventory.

        :return:
        """
        box_number = "BOX22222"
        bm = BoxManagementClass()

        # add a box with an invalid box type
        box_type_str = 'XXX'
        with raises(InvalidValueError):
            _ = bm.box_new(box_number=box_number, box_type=box_type_str)

        # add a box with a valid box type
        box_type_str = 'Evans'
        box_type = BoxType.objects.get(box_type_code=box_type_str)
        box = bm.box_new(box_number=box_number, box_type=box_type)
        assert box.box_number == box_number
        assert box.box_type == box_type
        assert box.location is None
        assert box.product is None
        assert box.exp_year is None
        assert box.exp_month_start is None
        assert box.exp_month_end is None
        assert box.date_filled is None
        assert box.quantity == box_type.box_type_qty

        # test attempting to create a duplicate box number
        with raises(InvalidActionAttemptedError):
            _ = bm.box_new(box_number=box_number, box_type=box_type_str)
        return

    def test_box_fill(self) -> None:
        """
        Test adding a box under various circumstances.

        :return:
        """
        # arbitrary values (except box number)
        box_number = 'BOX22368'
        location = '0101A1'
        product = 'Corn'
        exp_year = 2022
        exp_mo_start = 0
        exp_mo_end = 0
        date_time_filled = now()
        date_filled = date_time_filled.date()

        # add a new box to the inventory system
        bm = BoxManagementClass()
        _ = bm.box_new(box_number=box_number, box_type=2)

        # get records for above
        box_rec = Box.objects.select_related('box_type', ).get(
            box_number=box_number)
        box_type_rec = box_rec.box_type
        location_rec = Location.objects.select_related(
            'loc_row',
            'loc_bin',
            'loc_tier',
        ).get(loc_code=location)
        loc_row_rec = location_rec.loc_row
        loc_bin_rec = location_rec.loc_bin
        loc_tier_rec = location_rec.loc_tier
        product_rec = Product.objects.select_related('prod_cat', ).get(
            prod_name=product)
        prod_cat_rec = product_rec.prod_cat
        box_filled = bm.box_fill(
            box=box_rec,
            location=location_rec,
            product=product_rec,
            exp_year=exp_year,
            exp_mo_start=exp_mo_start,
            exp_mo_end=exp_mo_end
        )
        assert box_filled.box_number == box_number
        assert box_filled.box_type == box_type_rec
        assert box_filled.location == location_rec
        assert box_filled.product == product_rec
        assert box_filled.exp_year == exp_year
        assert box_filled.exp_month_start == exp_mo_start
        assert box_filled.exp_month_end == exp_mo_end
        # assert that the difference in date filled is less than 5 seconds
        assert abs(
            box_filled.date_filled - date_time_filled).total_seconds() < 5
        assert box_filled.quantity == box_type_rec.box_type_qty
        act_fill = Activity.objects.filter(
            box_number__exact=box_number,
            date_filled__exact=date_filled
        ).latest('-date_consumed')
        # NOTE - above ordering may be affected by the database provider
        assert act_fill.box_type == box_type_rec.box_type_code
        assert act_fill.loc_row == loc_row_rec.loc_row
        assert act_fill.loc_bin == loc_bin_rec.loc_bin
        assert act_fill.loc_tier == loc_tier_rec.loc_tier
        assert act_fill.prod_name == product_rec.prod_name
        assert act_fill.prod_cat_name == prod_cat_rec.prod_cat_name
        #  assuming starting and ending transaction are not over midnight
        assert act_fill.date_filled == date_filled
        assert act_fill.date_consumed is None
        assert act_fill.exp_year == exp_year
        assert act_fill.exp_month_start == exp_mo_start
        assert act_fill.exp_month_end == exp_mo_end
        assert act_fill.quantity == box_type_rec.box_type_qty
        assert act_fill.duration == 0
        assert act_fill.adjustment_code is None
        return

    def test_box_move(self) -> None:
        """
        Test moving a box under various circumstances.

        :return:
        """
        # starting box and target location
        box_number = 'BOX64346'
        target_location = '0409C2'
        bm = BoxManagementClass()

        # add a new box
        _ = bm.box_new(box_number=box_number, box_type=2)

        # fill it
        location = '0101A1'
        product = 'Corn'
        exp_year = 2022
        exp_mo_start = 0
        exp_mo_end = 0
        box_rec = Box.objects.select_related('box_type', ).get(
            box_number=box_number)
        location_rec = Location.objects.get(loc_code=location)
        product_rec = Product.objects.get(prod_name=product)
        _ = bm.box_fill(
            box=box_rec,
            location=location_rec,
            product=product_rec,
            exp_year=exp_year,
            exp_mo_start=exp_mo_start,
            exp_mo_end=exp_mo_end
        )

        # get the box just created and filled
        box_rec = Box.objects.select_related(
            'box_type',
            'product',
            'product__prod_cat',
        ).get(box_number=box_number)
        box_type_rec = box_rec.box_type
        product_rec = box_rec.product
        prod_cat_rec = product_rec.prod_cat
        exp_year = box_rec.exp_year
        exp_mo_start = box_rec.exp_month_start
        exp_mo_end = box_rec.exp_month_end
        date_time_filled = box_rec.date_filled
        date_filled = date_time_filled.date()

        # get the location record and associates for the target location
        location_rec = Location.objects.select_related(
            'loc_row',
            'loc_bin',
            'loc_tier',
        ).get(loc_code=target_location)
        loc_row_rec = location_rec.loc_row
        loc_bin_rec = location_rec.loc_bin
        loc_tier_rec = location_rec.loc_tier

        # move the box to a new location and save changes
        box_moved = bm.box_move(box_rec, location_rec)

        assert box_moved.box_number == box_number
        assert box_moved.box_type == box_type_rec
        assert box_moved.location == location_rec
        assert box_moved.product == product_rec
        assert box_moved.exp_year == exp_year
        assert box_moved.exp_month_start == exp_mo_start
        assert box_moved.exp_month_end == exp_mo_end
        assert box_moved.date_filled == date_time_filled
        assert box_moved.quantity == box_type_rec.box_type_qty

        # find the corresponding activity record
        act_moved = Activity.objects.filter(
            box_number__exact=box_number,
            date_filled__exact=date_filled,
        ).latest('-date_consumed')

        # box number part of filter above
        assert act_moved.box_type == box_type_rec.box_type_code
        assert act_moved.loc_row == loc_row_rec.loc_row
        assert act_moved.loc_bin == loc_bin_rec.loc_bin
        assert act_moved.loc_tier == loc_tier_rec.loc_tier
        assert act_moved.prod_name == product_rec.prod_name
        assert act_moved.prod_cat_name == prod_cat_rec.prod_cat_name
        # date filled part of filter above
        assert act_moved.date_consumed is None
        assert act_moved.exp_year == exp_year
        assert act_moved.exp_month_start == exp_mo_start
        assert act_moved.exp_month_end == exp_mo_end
        assert act_moved.quantity == box_type_rec.box_type_qty
        assert act_moved.duration == 0
        assert act_moved.adjustment_code is None
        return

    def test_box_consume(self) -> None:
        """
        Test consuming a box under various circumstances.

        :return:
        """
        # box to consume
        box_number = 'BOX12321'
        bm = BoxManagementClass()

        # add a new box
        _ = bm.box_new(box_number=box_number, box_type=2)

        # fill the box just added to inventory
        location = '0101A1'
        product = 'Corn'
        exp_year = 2022
        exp_mo_start = 0
        exp_mo_end = 0
        box_rec = Box.objects.get(box_number=box_number)
        location_rec = Location.objects.get(loc_code=location)
        product_rec = Product.objects.get(prod_name=product)
        _ = bm.box_fill(
            box=box_rec,
            location=location_rec,
            product=product_rec,
            exp_year=exp_year,
            exp_mo_start=exp_mo_start,
            exp_mo_end=exp_mo_end
        )

        # get the box just filled
        box_rec = Box.objects.select_related(
            'box_type',
            'location',
            'location__loc_row',
            'location__loc_bin',
            'location__loc_tier',
            'product',
            'product__prod_cat',
        ).get(box_number=box_number)
        box_type_rec = box_rec.box_type
        location_rec = box_rec.location
        loc_row_rec = location_rec.loc_row
        loc_bin_rec = location_rec.loc_bin
        loc_tier_rec = location_rec.loc_tier
        product_rec = box_rec.product
        prod_cat_rec = product_rec.prod_cat
        exp_year = box_rec.exp_year
        exp_mo_start = box_rec.exp_month_start
        exp_mo_end = box_rec.exp_month_end
        date_time_filled = box_rec.date_filled
        date_filled = date_time_filled.date()
        duration_time = now() - date_time_filled
        duration_days = duration_time.days

        # consume the box
        bm = BoxManagementClass()
        box_empty = bm.box_consume(box_rec)
        assert box_empty.box_number == box_number
        assert box_empty.box_type == box_type_rec
        assert box_empty.location is None
        assert box_empty.product is None
        assert box_empty.exp_year is None
        assert box_empty.exp_month_start is None
        assert box_empty.exp_month_end is None
        assert box_empty.date_filled is None
        assert box_empty.quantity is None

        # get the corresponding activity record
        act_consumed = Activity.objects.filter(
            box_number__exact=box_number,
            date_filled__exact=date_filled,
        ).latest('-date_consumed')
        assert act_consumed.box_type == box_type_rec.box_type_code
        assert act_consumed.loc_row == loc_row_rec.loc_row
        assert act_consumed.loc_bin == loc_bin_rec.loc_bin
        assert act_consumed.loc_tier == loc_tier_rec.loc_tier
        assert act_consumed.prod_name == product_rec.prod_name
        assert act_consumed.prod_cat_name == prod_cat_rec.prod_cat_name
        assert act_consumed.date_consumed == now().date()
        assert act_consumed.exp_year == exp_year
        assert act_consumed.exp_month_start == exp_mo_start
        assert act_consumed.exp_month_end == exp_mo_end
        assert act_consumed.quantity == box_type_rec.box_type_qty
        assert act_consumed.duration == duration_days
        assert act_consumed.adjustment_code is None
        return

    def test_pallet_finish(self) -> None:
        """
        Test loading and finishing off a pallet.

        Build a new pallet, add some boxes to it, stash the pallet id,
        the pallet box ids, and the box ids associated with them.  Then
        finish the pallet and make sure the pallet and all its pallet boxes
        have been deleted, while the boxes themselves have been preserved.
        Since we are going through the new and fill logic above, we are
        going to assume the activity records have been properly created.

        :return:
        """
        # set some arbitrary values
        pallet_name = 'Hopefully this never matches !@#$%^&*()_+'
        location_code = '0409C2'
        box_type_code = 'Evans'
        starting_box_number = 98765
        number_of_boxes = 40
        ending_box_number = starting_box_number + number_of_boxes
        product_choices = 'Corn', 'Green Beans'
        exp_year_choices = (now().year + 1), (now().year + 2)

        # get corresponding records
        box_type_rec = BoxType.objects.get(box_type_code=box_type_code)
        product1 = Product.objects.get(prod_name=product_choices[0])
        product2 = Product.objects.get(prod_name=product_choices[1])
        product_rec_choices = product1, product2

        bm = BoxManagementClass()

        # build the pallet
        location_rec = Location.objects.get(loc_code=location_code)
        pallet_rec = Pallet.objects.create(
            name=pallet_name,
            location=location_rec,
            pallet_status=Pallet.FILL,
        )
        pallet_rec_id = pallet_rec.id

        # build table of values for later comparison
        pallet_box_info = dict()
        for ndx, box_number in enumerate(
                range(starting_box_number, ending_box_number)):
            ind = ndx % 2
            box_name = BoxNumber.format_box_number(box_number)
            product = product_rec_choices[ind]
            exp_year = exp_year_choices[ind]
            box_rec = bm.box_new(box_number=box_name, box_type=box_type_rec)
            pallet_box_rec = PalletBox.objects.create(
                pallet=pallet_rec,
                box_number=box_name,
                box=box_rec,
                product=product,
                exp_year=exp_year,
                box_status=PalletBox.NEW
            )
            pallet_box_info[box_number] = PalletBoxInfo(
                pallet_box_id=pallet_box_rec.id, box_id=box_rec.id,
                box_number=box_name, product=product, exp_year=exp_year)

        # finish (publish) the pallet
        bm.pallet_finish(pallet_rec)

        # validate that worked properly
        for entry in pallet_box_info:
            with raises(PalletBox.DoesNotExist):
                _ = PalletBox.objects.get(
                    pk=pallet_box_info[entry].pallet_box_id
                )
            box_rec = Box.objects.get(pk=pallet_box_info[entry].box_id)
            assert box_rec.box_number == pallet_box_info[entry].box_number
            assert box_rec.box_type == box_type_rec
            assert box_rec.location == location_rec
            assert box_rec.product == pallet_box_info[entry].product
            assert box_rec.exp_year == pallet_box_info[entry].exp_year
            assert box_rec.exp_month_start == 0
            assert box_rec.exp_month_end == 0
            filled_seconds_ago = (now() - box_rec.date_filled).total_seconds()
            assert filled_seconds_ago < 10
            assert box_rec.quantity == box_type_rec.box_type_qty

        with raises(Pallet.DoesNotExist):
            _ = Pallet.objects.get(pk=pallet_rec_id)
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
