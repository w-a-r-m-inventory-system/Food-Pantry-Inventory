"""
BoxActivity.py - Record activity for changes to a box.
"""
from datetime import datetime, date
from enum import Enum, unique
from logging import getLogger, debug, error
from typing import Optional

from django.db import transaction, IntegrityError
from django.utils.timezone import now

from fpiweb.constants import InternalError
from fpiweb.models import Box, Activity

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "07/31/2019"


# "${Copyright.py}"


@unique
class BOX_ACTION(Enum):
    """
    Actions to be applied to a box.
    """
    FILL: str = 'fill'
    MOVE: str = 'move'
    EMPTY: str ='empty'

log = getLogger('fpiweb')


class BoxActivityClass:
    """
    BoxManagementClass - Manage db for changes to a box.
    """

    def __init__(self):

        # holding area for records that are being added or modified
        self.box: Optional[Box] = None
        self.activity: Optional[Activity] = None

    def box_add(self, box_id: int):
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
        self.box = Box.objects.select_related('product').select_related(
            'product__prod_cat').select_related('box_type').get(id=box_id)

        # determine if there is a prior open activity record
        # try:
        activity_set = Activity.objects.filter(
            box_number__exact=self.box.box_number).order_by(
            'date_filled'
        )
        if len(activity_set) > 0:
            activity = activity_set[0]
            if activity.date_consumed:
                # box previously emptied - expected
                self.activity = None
            else:
                # oops - empty box before filling it again
                self.activity = activity
                self._consume_activity(
                    adjustment=Activity.ADD_EMPTIED
                )
                self.activity = None
        else:
            self.activity = None
        # except Activity.DoesNotExist:
        #     # expected - first time box number is used
        #     pass

        # back on happy path
        self._add_activity()
        return

    def box_move(self, box_id: int):
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
        :param new_loc: internal location ID of new location
        :return:
        """

        # get the box record for this id
        self.box = Box.objects.get(id=box_id)

        # find the prior open activity record
        # try:
        self.activity = Activity.objects.get(
            box_number=self.box.box_number,
            date_filled=self.box.date_filled
        )
        if self.activity:
            # found an activity record, check it out
            if self.activity.date_consumed:
                # oops - box has no open activity record so create one
                self.activity = None
                self._add_activity(
                    adjustment=Activity.MOVE_ADDED
                )
            else:
                # expected - has open activity record
                pass
        else:
            # oops - box has no open activity record so create one
            self.activity = None
            self._add_activity(
                adjustment=Activity.MOVE_ADDED
            )
        # except Activity.DoesNotExist:
        #     # oops - box has no open activity record so create one
        #     self.activity = None
        #     self._add_activity(
        #         adjustment=Activity.MOVE_ADDED
        #     )

        # back on happy path - update location
        self._update_activity_location()
        return

    def box_empty(self, box_id: int):
        """
        Record activity for a box being emptied (consumed).

        This method expects the box record to still have the location,
        product, etc. information still in it.  After reording the
        appropriate information in the activity record, this method will
        clear out the box so it will be empty again.

        :param box_id:
        :return:
        """
        # get the box record for this id
        self.box = Box.objects.select_related('product').select_related(
            'product__prod_cat').select_related('box_type').get(id=box_id)

        # determine if there is a prior open activity record
        try:
            self.activity = Activity.objects.filter(
                box_number__exact=self.box.box_number).get_latest_by(
                'date_filled'
            )
            if self.activity.date_consumed:
                # oops - this activity record already consumed, make another
                self.activity = None
                self._add_activity(
                    adjustment=Activity.CONSUME_ADDED
                )
            else:
                # expected
                pass
        except Activity.DoesNotExist:
            # oops - box has no open activity record so create one
            self.activity = None
            self._add_activity(
                adjustment=Activity.CONSUME_ADDED
            )

        # back on happy path
        self._consume_activity()
        return

    def _add_activity(self, adjustment: str = None):
        """
        Add a new activity record based on this box.

        :param adjustment:
        :return:
        """
        try:
            # with transaction.atomic:
                self.activity = Activity(
                    box_number=self.box.box_number,
                    box_type=self.box.box_type.box_type_code,
                    loc_row=self.box.loc_row,
                    loc_bin=self.box.loc_bin,
                    loc_tier=self.box.loc_tier,
                    prod_name=self.box.product.prod_name,
                    prod_cat_name=self.box.product.prod_cat.prod_cat_name,
                    date_filled=self.box.date_filled,
                    date_consumed=None,
                    duration=0,
                    exp_year=self.box.exp_year,
                    exp_month_start=self.box.exp_month_start,
                    exp_month_end=self.box.exp_month_end,
                    quantity=self.box.box_type.box_type_qty,
                    adjustment_code=adjustment,
                )
                self.activity.save()
        except IntegrityError as exc:
            # report an internal error
            self._report_internal_error(
                exc, 'adding an activity for a newly filled box'
            )
        # self.activity = None
        return

    def _update_activity_location(self):
        """
        Update the location in the activity record.

        :param box_id:
        :return:
        """
        try:
            # with transaction.atomic():
                self.activity.loc_row=self.box.loc_row
                self.activity.loc_bin=loc_bin=self.box.loc_bin
                self.activity.loc_tier=loc_tier=self.box.loc_tier
                self.activity.save()
        except IntegrityError as exc:
            # report an internal error
            self._report_internal_error(
                exc, 'update a activity by moving a box'
            )
        self.activity = None
        return

    def _consume_activity(self, adjustment: str = None):
        """
        Mark this activity record consumed based on this box.

        :param box_id:
        :return:
        """
        try:
            with transaction.atomic():
                date_filled = self.activity.date_filled
                filled = date(
                    date_filled.year, date_filled.month, date_filled.day
                )
                date_consumed = now()
                consumed = date(
                    date_consumed.year, date_consumed.month, date_consumed.day
                )
                duration = consumed - filled
                self.activity = Activity(
                    date_consumed=now(),
                    duration=duration
                )
                # if this is not an adjustment, preserve previous entry
                if not self.activity.adjustment_code:
                    self.activity = Activity(adjustment_code=adjustment)
                self.activity.save()
        except IntegrityError as exc:
            # report an internal error
            self._report_internal_error(
                exc, 'update an activity by consuming a box'
            )
        self.activity = None
        return

    def _report_internal_error(self, exc: Exception, action: str):
        """
        Report details of an internal error
        :param exp: original exeception
        :param action: additional message
        :return: (no return, ends by raising an additional exception
        """
        # report an internal error
        if self.box is None:
            box_number = 'is missing'
        else:
            box_number = self.box.box_number
        if self.activity is None:
            activity_info = f'is empty (as expected)'
        else:
            if self.activity.date_consumed:
                date_consumed = self.activity.date_consumed
            else:
                date_consumed = '(still in inventory)'
            activity_info = (
                f'has box {self.activity.box_number}, created '
                f'{self.activity.date_filled}, consumed {date_consumed}'
            )
        error(
            f'Got error: {exc}'
            f'while attempting to {action}, Box info: '
            f'{box_number}, Activity info: {activity_info}'
        )
        raise InternalError('Internal error, see log for details')

# EOF
