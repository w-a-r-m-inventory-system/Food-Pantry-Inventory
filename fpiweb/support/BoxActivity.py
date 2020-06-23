"""
BoxActivity.py - Record activity for changes to a box.

Error messages from this module are prefixed by 2nn, e.g. "201 - blah blah..."

"""
from datetime import datetime, date
from enum import Enum, unique
from logging import getLogger
from typing import Optional

from django.db import transaction, IntegrityError
from django.utils.timezone import now

from fpiweb.constants import \
    InternalError
from fpiweb.models import \
    Box, \
    Activity, \
    BoxType, \
    Location, \
    LocRow, \
    LocBin, \
    LocTier, \
    Product, \
    ProductCategory

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "07/31/2019"

# "${Copyright.py}"


logger = getLogger('fpiweb')


@unique
class BOX_ACTION(Enum):
    """
    Actions to be applied to a box.
    """
    ADD: str = 'add'         # add a new (empty) box to inventory
    FILL: str = 'fill'       # fill an empty box with product
    MOVE: str = 'move'       # move a box from one location to another
    EMPTY: str = 'empty'     # empty (consume) a box of product


class BoxActivityClass:
    """
    BoxManagementClass - Manage db for changes to a box.

    I decided that (for now) empty boxes should not be added to the activity
    records.  Activity records will show only when a box was filled or
    emptied.  The activity records for filled boxes will show only their
    current location.  Activity records for consumed boxes will show their
    last location. (tr)

    For now, the activity records will not show empty boxes, damaged or
    discarded boxes removed from the inventory system.
    """

    def __init__(self):

        # holding area for records that are being added or modified
        self.box: Optional[Box] = None
        self.box_type: Optional[BoxType] = None
        self.location: Optional[Location] = None
        self.loc_row: Optional[LocRow] = None
        self.loc_bin: Optional[LocBin] = None
        self.loc_tier: Optional[LocTier] = None
        self.product: Optional[Product] = None
        self.prod_cat: Optional[ProductCategory] = None
        self.activity: Optional[Activity] = None

    def box_new(self, box_id: Box.id):
        """
        Record that a new (empty) box has been added to inventory.

        :param box_id: internal box ID of box being added to inventory
        :return:
        """
        # =============================================================== #
        # No activity records for new boxes for now.  See note above.
        # =============================================================== #
        # try:
        #     self.box = Box.objects.select_related('boxtype').get(pk=box_id)
        # except Box.DoesNotExist:
        #     raise InternalError(
        #         f'201 - New box for {box_id} not successfully created'
        #     )
        # self.activity = Activity.objects.create(
        #     box_number=self.box.box_number,
        #     box_type=self.box.box_type.box_type_code,
        # )
        logger.debug(f'Act Box New: No action - Box ID: {box_id}')
        return

    def box_fill(self, box_id: Box.id):
        """
        Record activity for a box being filled and added to inventory.

        This method expects that the box record already has the box
        type. location, product, and expiration date filled in.

        This method will write a new activity record that "starts the
        clock" for this box.  If the box was already marked as checked
        in to inventory, the previous contents will be checked out and
        the new contents checked in.

        :param box_id: internal box ID of box being added to inventory
        :return:
        """

        # get the box record and related records for this id
        self.box = Box.objects.select_related(
            'box_type',
            'location',
            'location__loc_row',
            'location__loc_bin',
            'location__loc_tier',
            'product',
            'product__prod_cat',
        ).get(id=box_id)
        self.box_type = self.box.box_type
        self.location = self.box.location
        self.loc_row = self.location.loc_row
        self.loc_bin = self.location.loc_bin
        self.loc_tier = self.location.loc_tier
        self.product = self.box.product
        self.prod_cat = self.product.prod_cat
        logger.debug(f'Act Box Fill: box received: Box ID: {box_id}')

        # determine if the most recent activity record (if any) was
        # consumed.  If it was, start a new one.  If not, mark the product
        # in the old activity record as consumed and start a new activity
        # record for the product just added to the box.
        self.activity = None
        try:
            self.activity = Activity.objects.filter(
                box_number__exact=self.box.box_number).latest(
                '-date_filled', '-date_consumed')
            # NOTE - above ordering may be affected by the database provider
            logger.debug(
                f'Act Box Fill: Latest activity found: '
                f'{self.activity.box_number}, '
                f'filled:{self.activity.date_filled}'
            )
            if self.activity.date_consumed:
                # box previously emptied - expected
                logger.debug(
                    f'Act Box Fill: Previous activity consumed: '
                    f'{self.activity.date_consumed}'
                )
                self.activity = None
            else:
                # oops - empty box before filling it again
                logger.debug(f'Act Box Fill: Consuming previous box contents')
                self._consume_activity(adjustment=Activity.FILL_EMPTIED)
                self.activity = None
        except Activity.DoesNotExist:
            # no previous activity for this box
            self.activity = None
            logger.debug(f'Act Box Fill: No previous activity found')

        # back on happy path
        self._add_activity()
        logger.debug(f'Act Box Fill: done')
        return

    def box_move(self, box_id: Box.id):
        """
        Record activity for a box being moved in tne inventory.

        This method expects that the box record already has the box
        type. location, product, and expiration date filled in.

        This method will change the current location of the box in the
        activity record.  The old location will not be retained nor will
        any "clocks" for the activity record be updated.

        If the box does not have an open activity record, a new one will be
        created.

        :param box_id: internal box ID of box being moved
        :return:
        """

        # get the box record for this id and related records in case needed
        logger.debug(f'Act Box Move: box received: Box ID: {box_id}')
        self.box = Box.objects.select_related(
            'box_type',
            'location',
            'location__loc_row',
            'location__loc_bin',
            'location__loc_tier',
            'product',
            'product__prod_cat',
        ).get(id=box_id)
        self.box_type = self.box.box_type
        self.location = self.box.location
        self.loc_row = self.location.loc_row
        self.loc_bin = self.location.loc_bin
        self.loc_tier = self.location.loc_tier
        self.product = self.box.product
        self.prod_cat = self.product.prod_cat

        # find the prior open activity record
        # note: there should be only one box, but with bad data there may be
        # more than one activity record that qualifies.  Deal with it by
        # keeping a matching one (if found) and fill all the others.
        try:
            act_for_box = Activity.objects.filter(
                box_number=self.box.box_number,
                date_consumed=None,
            ).order_by('-date_filled')

            # look for one closely matching activity record and consume all
            # the others with an adjustment code
            self.activity = None
            for act in act_for_box:
                if (not self.activity) and (
                            act.box_type == self.box_type.box_type_code and
                            # cannot compare location because the box has
                            # already been marked as moved
                            act.prod_name == self.product.prod_name and
                            act.date_filled == self.box.date_filled.date() and
                            act.exp_year == self.box.exp_year and
                            act.exp_month_start == self.box.exp_month_start and
                            act.exp_month_end == self.box.exp_month_end
                        ):
                    self.activity = act
                else:
                    # consume this bogus open activity record now
                    date_consumed, duration = self.compute_duration_days(
                        act.date_filled)
                    act.date_consumed = date_consumed
                    act.duration = duration
                    act.adjustment_code = Activity.MOVE_CONSUMED
                    logger.debug(
                        f'Act Box Move: Bogus open activity found for: '
                        f'{act.box_number}, '
                        f'filled:{act.date_filled}, '
                        f'Forced to be consumed now'
                    )
                    act.save()
            if self.activity:
                logger.debug(
                    f'Act Box Move: Activity found to move: '
                    f'{self.activity.box_number}, '
                    f'filled:{self.activity.date_filled}'
                )
            else:
                logger.debug(
                    f'Act Box Move: Activity not consumed - proceeding...')
                raise Activity.DoesNotExist
        except Activity.DoesNotExist:
            # oops - box has no open activity record so create one
            self.activity = None
            logger.debug(
                f'Act Box Move: Activity for this box missing - making a '
                f'new one...'
            )
            self._add_activity(
                adjustment=Activity.MOVE_ADDED
            )
        # Let Activity.MultipleObjectsReturned error propagate.

        # back on happy path - update location
        logger.debug(f'Act Box Move: Updating activity ID: {self.activity.id}')
        self._update_activity_location()
        logger.debug(f'Act Box Move: done')
        return

    def box_empty(self, box_id: Box.id):
        """
        Record activity for a box being emptied (consumed).

        This method expects the box record to still have the location,
        product, etc. information still in it.  After recording the
        appropriate information in the activity record, this method will
        clear out the box so it will be empty again.

        :param box_id:
        :return:
        """
        # get the box record for this id
        self.box = Box.objects.select_related(
            'box_type',
            'location',
            'location__loc_row',
            'location__loc_bin',
            'location__loc_tier',
            'product',
            'product__prod_cat',
        ).get(id=box_id)
        self.box_type = self.box.box_type
        self.location = self.box.location
        self.loc_row = self.location.loc_row
        self.loc_bin = self.location.loc_bin
        self.loc_tier = self.location.loc_tier
        self.product = self.box.product
        self.prod_cat = self.product.prod_cat
        logger.debug(f'Act Box Empty: box received: Box ID: {box_id}')

        # determine if there is a prior open activity record
        try:
            self.activity = Activity.objects.filter(
                box_number__exact=self.box.box_number).latest(
                'date_filled', '-date_consumed'
            )
            logger.debug(
                f'Act Box Empty: Activity found - id: '
                f'{self.activity.id}, filled: {self.activity.date_filled}'
            )

            if self.activity.date_consumed:
                # oops - this activity record already consumed, make another
                logger.debug(
                    f'Act Box Empty: activity consumed '
                    f'{self.activity.date_consumed}, make new activity'
                )
                self.activity = None
                self._add_activity(adjustment=Activity.CONSUME_ADDED)
            elif (
                    self.activity.loc_row !=
                    self.loc_row.loc_row or
                    self.activity.loc_bin !=
                    self.loc_bin.loc_bin or
                    self.activity.loc_tier !=
                    self.loc_tier.loc_tier or
                    self.activity.prod_name != self.product.prod_name or
                    self.activity.date_filled != self.box.date_filled.date() or
                    self.activity.exp_year != self.box.exp_year or
                    self.activity.exp_month_start !=
                    self.box.exp_month_start or
                    self.activity.exp_month_end != self.box.exp_month_end
            ):
                # some sort of mismatch due to the box being emptied and
                # refilled without notifying the inventory system
                logger.debug(
                    f'Act Box Empty: mismatch, consume this activity and '
                    f'make a new one'
                )
                self._consume_activity(
                    adjustment=Activity.CONSUME_ADDED)
                self._add_activity(adjustment=Activity.CONSUME_EMPTIED)
            else:
                # expected
                logger.debug(
                    f'Act Box Empty: box and activity matched, record '
                    f'consumption '
                )
                pass
        except Activity.DoesNotExist:
            # oops - box has no open activity record so create one
            self.activity = None
            logger.debug(f'Act Box Empty: no activity, make one')
            self._add_activity(
                adjustment=Activity.CONSUME_ADDED
            )

        # back on happy path
        self._consume_activity()
        logger.debug(f'Act Box Empty: done')
        return

    def _add_activity(self, adjustment: str = None):
        """
        Add a new activity record based on this box.

        :param adjustment:
        :return:
        """
        try:
            with transaction.atomic():
                self.activity = Activity(
                    box_number=self.box.box_number,
                    box_type=self.box_type.box_type_code,
                    loc_row=self.loc_row.loc_row,
                    loc_bin=self.loc_bin.loc_bin,
                    loc_tier=self.loc_tier.loc_tier,
                    prod_name=self.product.prod_name,
                    prod_cat_name=self.prod_cat.prod_cat_name,
                    date_filled=self.box.date_filled.date(),
                    date_consumed=None,
                    duration=0,
                    exp_year=self.box.exp_year,
                    exp_month_start=self.box.exp_month_start,
                    exp_month_end=self.box.exp_month_end,
                    quantity=self.box.quantity,
                    adjustment_code=adjustment,
                )
                self.activity.save()
                logger.debug(
                    f'Act Box_Add: Just added activity ID: '
                    f'{self.activity.id}'
                )
        except IntegrityError as exc:
            # report an internal error
            self._report_internal_error(
                exc,
                'adding an activity for a newly filled box'
            )
        return

    def _update_activity_location(self):
        """
        Update the location in the activity record.

        :return:
        """
        try:
            with transaction.atomic():
                self.activity.loc_row = self.loc_row.loc_row
                self.activity.loc_bin = self.loc_bin.loc_bin
                self.activity.loc_tier = self.loc_tier.loc_tier
                self.activity.save()
                logger.debug(
                    f'Act Box_Upd: Just updated activity ID: '
                    f'{self.activity.id}'
                )
                self.activity.save()
        except IntegrityError as exc:
            # report an internal error
            self._report_internal_error(
                exc,
                'update an activity by moving a box'
            )
        self.activity = None
        return

    def _consume_activity(self, adjustment: str = None):
        """
        Mark this activity record consumed based on this box.

        :param adjustment:
        :return:
        """
        try:
            with transaction.atomic():
                # update activity record
                date_consumed, duration = self.compute_duration_days(
                    self.activity.date_filled)
                self.activity.date_consumed = date_consumed
                self.activity.duration = duration
                # if this is not an adjustment, preserve previous entry
                if not self.activity.adjustment_code:
                    self.activity.adjustment_code = adjustment
                self.activity.save()
                logger.debug(
                    f'Act Box_Empty: Just consumed activity ID: '
                    f'{self.activity.id}'
                )

                # update box record but only if on happy path
                if not adjustment:
                    self.box.location = None
                    self.box.product = None
                    self.box.exp_year = None
                    self.box.exp_month_start = None
                    self.box.exp_month_end = None
                    self.box.date_filled = None
                    self.box.quantity = None
                    self.box.save()
                    logger.debug(
                        f'Act Box_Empty: Just emptied box ID: {self.box.id}'
                    )
        except IntegrityError as exc:
            # report an internal error
            self._report_internal_error(
                exc,
                'update an activity by consuming a box'
            )
        self.activity = None
        return

    def compute_duration_days(self, date_filled: date) -> tuple:
        """
        compute the days between the date filled and today

        :param date_filled:
        :return: tuple of date consumed and number of days in box
        """
        date_consumed = now().date()
        duration = (date_consumed - date_filled).days
        return date_consumed, duration

    def _report_internal_error(self, exc: Exception, action: str):
        """
        Report details of an internal error
        :param exc: original exeception
        :param action: additional message
        :return: (no return, ends by raising an additional exception
        """
        # report an internal error
        if self.box is None:
            box_number = 'is missing'
        else:
            box_number = self.box.box_number
        if self.activity is None:
            activity_info = f'activity missing'
        else:
            if self.activity.date_consumed:
                date_consumed = self.activity.date_consumed
            else:
                date_consumed = '(still in inventory)'
            activity_info = (
                f'has box {self.activity.box_number}, created '
                f'{self.activity.date_filled}, consumed '
                f'{date_consumed}'
            )
        logger.error(
            f'Got error: {exc}'
            f'while attempting to {action}, Box info: '
            f'{box_number}, Activity info: {activity_info}'
        )
        raise InternalError('Internal error, see log for details')

# EOF
