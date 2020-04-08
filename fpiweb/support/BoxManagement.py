"""
BoxManagement.py - Manage box creating, filling, moving and emptying.

Error messages from this module are prefixed by 1nn, e.g. "101 - blah blah..."
"""

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "01/11/2020"

# "${Copyright.py}"
from typing import Optional, Union

from django.db import transaction
from django.utils.timezone import now

from fpiweb.constants import \
    InvalidValueError, \
    InvalidActionAttemptedError, \
    CURRENT_YEAR
from fpiweb.models import \
    Box, \
    Pallet, \
    PalletBox, \
    Location, \
    Product, \
    BoxType, \
    BoxNumber, \
    Constraints
from fpiweb.support.BoxActivity import BoxActivityClass


class BoxManagementClass:
    """
    BoxManagementClass - Manage db changes for box changes.

    The public API's validate parameter values.  The private methods
    perform the actual actions.
    """

    def __init__(self):
        self.pallet: Optional[Pallet] = None
        self.pallet_box: Optional[PalletBox] = None
        self.box: Optional[Box] = None
        self.box_type: Optional[BoxType] = None
        self.location: Optional[Location] = None
        self.product: Optional[Product] = None
        self.exp_year: Optional[int] = None
        self.exp_mo_start: Optional[int] = None
        self.exp_mo_end: Optional[int] = None
        self.activity = BoxActivityClass()

    def box_new(self, box_number: str,
                box_type: Union[str, int, BoxType]) -> Box:
        """
        Add a new empty box to the inventory system.  If successful it
        adds an activity record for an empty box and returns the box record
        just created.

        Requirements:

        *   Box number is valid, unique, and not previously assigned

        *   Box type is valid

        Exceptions:

            101 - Box number supplied is not in the valid format ('BOXnnnn')

            102 - Box number is not unique

            102 - Box type is not valid

        :param box_number: in the form of 'BOXnnnnn'
        :param box_type: a valid box type code, BoxType record or record id
        :return: the newly created box record
        """

        # box number validation
        if not BoxNumber.validate(box_number):
            raise InvalidValueError(f'101 - Box number of "{box_number}" is '
                                    f'improperly formatted or missing')

        box_exists_qs = Box.objects.filter(box_number=box_number)
        if len(box_exists_qs) > 0:
            raise InvalidActionAttemptedError(
                f'102 - Creating a new box {box_number} failed because it'
                f'already exists')

        # box type validation - either code, id or record
        if type(box_type) == BoxType:
            self.box_type = box_type
        elif type(box_type) == int:
            try:
                self.box_type = BoxType.objects.get(pk=box_type)
            except BoxType.DoesNotExist:
                raise InvalidValueError(
                    f'102 - Box type id of "{box_type}" is invalid')
        else:
            try:
                self.box_type = BoxType.objects.get(box_type_code=box_type)
            except BoxType.DoesNotExist:
                raise InvalidValueError(
                    f'102 - Box type code of "{box_type}" is invalid')
        self._new_box(box_number, self.box_type)
        return self.box

    def box_fill(self, *,
                 box: Union[Box, int],
                 location: Union[Location, int],
                 product: Union[Product, int],
                 exp_year: int,
                 exp_mo_start: int = 0,
                 exp_mo_end: int = 0
                 ):
        """
        Fill an individual box with product and add to the inventory.  If
        the box is not empty, an activity record will empty the box of its
        previous contents and a new activity record will note the new
        contents profiled.  If successful, it will return the box just
        filled.

        Requirements:

        *   Box record has not been modified

        *   All required fields are valid

        *   Optional month start and end, if specified, bracket one or
            more months

        Exceptions:

            111 - Attempting to fill a box that does not exist

            112 - location supplied is not valid

            113 - the product supplied is not valid

            114 - the expiration  year, start month, and/or end month are
                not valid or are out of range

        :param box: Box record or id of a box already in the system
        :param location: Target location record or ID
        :param product: Target product record or ID
        :param exp_year: year (current year +/- 10)
        :param exp_mo_start: 1 - 12 if specified - usually beginning quarter
        :param exp_mo_end: 1-12 if specified - usually ending quarter
        :return: box record after modifications
        """
        if type(box) == Box:
            self.box = box
        else:
            try:
                self.box = Box.objects.select_related('box_type').get(pk=box)
            except Box.DoesNotExist:
                raise InvalidActionAttemptedError(
                    f'111 - Attempting to fill a box that does not exist.  ID '
                    f'given was "{box}"')
        if type(location) == Location:
            self.location = location
        else:
            try:
                self.location = Location.objects.get(pk=location)
            except Location.DoesNotExist:
                raise InvalidValueError(
                    f'112 - Location with ID "{location}" not found')
        if type(product) == Product:
            self.product = product
        else:
            try:
                self.product = Product.objects.get(pk=product)
            except Product.DoesNotExist:
                raise InvalidValueError(
                    f'113 - Product with ID "{product}" not found')

        # presume the date information is true until proven otherwise
        expiration_info_valid = True

        years_ahead_list = Constraints.get_values(
            Constraints.FUTURE_EXP_YEAR_LIMIT)
        years_ahead = years_ahead_list[0]
        future_exp_year_limit = CURRENT_YEAR + years_ahead
        if exp_year < CURRENT_YEAR or exp_year > future_exp_year_limit:
            expiration_info_valid = False
        else:
            self.exp_year = exp_year

        # both valid months or zero or null
        if (exp_mo_start is None) or exp_mo_start == 0:
            self.exp_mo_start = 0
        elif 1 <= exp_mo_start <= 12:
            self.exp_mo_start = exp_mo_start
        else:
            expiration_info_valid = False

        if (exp_mo_end is None) or exp_mo_end == 0:
            self.exp_mo_end = 0
        elif 1 <= exp_mo_end <= 12:
            self.exp_mo_end = exp_mo_end
        else:
            expiration_info_valid = False

        # end must be greater than or equal to start
        if self.exp_mo_end < self.exp_mo_start:
            expiration_info_valid = False

        # did it pass the gauntlet?
        if not expiration_info_valid:
            raise InvalidValueError(
                f'114 - Expiration date information of {exp_mo_start} -'
                f' {exp_mo_end} - {exp_year} was not valid')
        self._fill_box()
        return self.box

    def box_move(self, box: Union[Box, int], location: Union[Location, int]):
        """
        Move an individual box in the inventory.  The activity record for
        this box will be changed to show  the new location.  The old
        location will be dropped from the activity record.  If successful,
        the box record will be returned.

        Requirements:

        *   Box is filled

        *   Location is valid

        Exceptions:

            121 - Box not in system

            122 - Cannot move an empty box

            123 - Location is not valid

        :param box:
        :param location:
        :return:
        """
        if type(box) == Box:
            self.box = box
        else:
            try:
                self.box = Box.objects.get(pk=box).select_related('box_type')
            except Box.DoesNotExist:
                raise InvalidActionAttemptedError(
                    f'121 - Attempting to move a box that does not exist.  ID '
                    f'given was "{box}"')
        if not self.box.product:
            raise InvalidActionAttemptedError(
                f'122 - Attempting to move an empty box')
        if type(location) == Location:
            self.location = location
        else:
            try:
                self.location = Location.objects.get(pk=location)
            except Location.DoesNotExist:
                raise InvalidValueError(
                    f'123 - Location with ID "{location}" not found')
        self._move_box()
        return self.box

    def box_consume(self, box: Union[Box, int]) -> Box:
        """
        Consume (e.g. empty) a box.  The box will be marked empty,
        the activity record will be updated, and the box will be returned.

        Requirements:

        *   The box must not be empty when passed in.

        Exception:

            131 - Box not in system

            132 - The box was already empty

        :param box:
        :return: the box record freshly emptied
        """
        if type(box) == Box:
            self.box = box
        else:
            try:
                self.box = Box.objects.select_related('box_type').get(pk=box)
            except Box.DoesNotExist:
                raise InvalidActionAttemptedError(
                    f'131 - Attempting to move a box that does not exist.  ID '
                    f'given was "{box}"')
        if not self.box.product:
            raise InvalidActionAttemptedError(
                f'132 - Attempting to consume the contents of an empty box')

        self._consume_box()
        return self.box

    def pallet_finish(self, pallet: Union[Pallet, int, str]):
        """
        Finish the processing of a pallet  of boxes into inventory.  Each
        box of the pallet will be processed.  Nothing will be returned.

        Note - a pallet is still considered valid even if there are no
        boxes associated with it.

        Requirements:

        *   A valid pallet record, pallet name, or ID

        *   A pallet status indicating if the boxes have just been filled
            or are being moved to a new location

        Exception:

            161 - An invalid pallet ID was passed in

            162 - An invalid pallet name was passed in

            166 - The pallet has an invalid location

        :param pallet:
        :return:
        """
        if type(pallet) == Pallet:
            pallet_rec = pallet
        elif type(pallet) == int:
            try:
                pallet_rec = Pallet.objects.get(pk=pallet)
            except Pallet.DoesNotExist:
                raise InvalidValueError(
                    f'161 - A pallet with ID: {pallet} does not exist')
        else:
            try:
                pallet_rec = Pallet.objects.get(name=pallet)
            except Pallet.DoesNotExist:
                raise InvalidValueError(
                    f'162 - A pallet with the name "{pallet}" does not '
                    f'currently exist')
        try:
            location = Location.objects.get(pk=pallet_rec.location.id)
        except Location.DoesNotExist:
            raise InvalidValueError(
                f'166 - The location of "{pallet_rec.location}" does not '
                f'exist')
        # TODO Mar 19 2020 travis - temporary fix
        pallet_status = pallet.pallet_status
        if pallet_status is None or pallet_status.strip() == '':
            pallet_status = Pallet.FILL
        pallet_boxes = PalletBox.objects.filter(pallet=pallet_rec)
        # transfer info and delete the pallet and its boxes in one trans
        with transaction.atomic():
            if pallet_status == Pallet.FILL:
                # transfer the information to the real boxes
                for pallet_box in pallet_boxes:
                    box = pallet_box.box
                    product = pallet_box.product
                    exp_year = pallet_box.exp_year
                    exp_mo_start = pallet_box.exp_month_start
                    exp_mo_end = pallet_box.exp_month_end
                    self.box_fill(
                        box=box,
                        location=location,
                        product=product,
                        exp_year=exp_year,
                        exp_mo_start=exp_mo_start,
                        exp_mo_end=exp_mo_end,
                    )
            else:
                # move or merge the boxes to the new location
                for pallet_box in pallet_boxes:
                    box = pallet_box.box
                    self.box_move(
                        box=box,
                        location=location,
                    )

            # delete the pallet boxes for this pallet en mass
            pallet_boxes.delete()
            # now delete the pallet itself
            pallet_rec.delete()
        return

    def _new_box(self, box_number: str, box_type: BoxType):
        """
        Add a new, uniquely numbered box to the inventory system.

        :param box_number:
        :param box_type:
        :return:
        """
        with transaction.atomic():
            self.box = Box.objects.create(box_number=box_number,
                                          box_type=box_type,
                                          quantity=box_type.box_type_qty)
        self.activity.box_new(self.box.id)
        return

    def _fill_box(self):
        """
        Fill a supposedly empty box and record activity for the event.

        :return:
        """
        with transaction.atomic():
            self.box.location = self.location
            self.box.product = self.product
            self.box.exp_year = self.exp_year
            self.box.exp_month_start = self.exp_mo_start
            self.box.exp_month_end = self.exp_mo_end
            self.box.date_filled = now()
            self.box.quantity = self.box.box_type.box_type_qty
            self.box.save()

            self.activity.box_fill(self.box.id)
        return

    def _move_box(self):
        """
        Move a filled box to a new location.

        :return:
        """
        with transaction.atomic():
            self.box.location = self.location
            self.box.save()

            self.activity.box_move(self.box.id)
        return

    def _consume_box(self):
        """
        Mark the box as empty.

        :return:
        """
        # We are passing the box on to the activity class unchanged because
        # that method needs to see the former contents.  This is so that if
        # someone has emptied the box and refilled it with something else,
        # the previous contents need to be consumed as well as the contents
        # just emptied.  That method will clear out the box before returning.
        self.activity.box_empty(self.box.id)

        # since we didn't modify the box ourself, we have a stale copy of
        # the box record.  Refresh it.
        box_id = self.box.id
        try:
            self.box = Box.objects.get(pk=box_id)
        except Box.DoesNotExist as exc:
            self.activity._report_internal_error(exc,
                                                 f'Box with ID {id} disappeared after consume processing')
        return


if __name__ == "__main__":
    box_mgmt = BoxManagementClass()

# EOF
