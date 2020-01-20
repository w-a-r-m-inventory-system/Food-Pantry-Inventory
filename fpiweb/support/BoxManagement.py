"""
BoxManagement.py - Manage box creating, filling, moving and emptying.
"""

from logging import getLogger, debug, error

__author__ = 'Travis Risner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "01/11/2020"

# "${Copyright.py}"
from typing import Optional, Union

from fpiweb.models import Box, Pallet, PalletBox, Location, Product, BoxType
from fpiweb.support.BoxActivity import BoxActivityClass


class BoxManagementClass:
    """
    BoxManagementClass - Manage db changes for box changes.
    """

    def __init__(self):
        self.pallet: Optional[Pallet] = None
        self.pallet_box: Optional[PalletBox] = None
        self.box: Optional[Box] = None
        self.location: Optional[Location] = None
        self.product: Optional[Product] = None
        self.exp_year: Optional[int] = None
        self.exp_mo_start: Optional[int] = None
        self.exp_mo_end: Optional[int] = None
        self.activity = BoxActivityClass()

    def box_new(self, box_number: str, box_type: BoxType) -> Box:
        """
        Add a new empty box to the inventory system.  If successful it
        adds an activity record for an empty box and returns the box record
        just created.

        Requirements:

        *   Box number is valid, unique, and not prevously assigned

        *   Box type is valid

        Exceptions:

            xxx - Box number supplied is not in the valid format ('BOXnnnn')

            xxx - Box number is not unique

            xxx - Box type is not valid

        :param box_number: in the form of 'BOXnnnnn'
        :param box_type: a valid box type
        :return: the newly created box record
        """
        self.box = Box()
        self.box.box_number = box_number
        self.box.box_type = box_type
        return self.box

    def box_fill(
            self, box: Union[Box, int], location: Union[Location, int],
            product: Union[Product, int], exp_year: int,
            exp_mo_start: int = 0, exp_mo_end: int = 0):
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

            xxx - location supplied is not valid

            xxx - the product supplied is not valid

            xxx - the expiration  year, start month, and/or end month are
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
            self.box = Box()
            self.box.id = box
        if type(location) == Location:
            self.location = location
        else:
            self.location = Location()
        if type(product) == Product:
            self.product = product
        else:
            self.product = Product()
        self.exp_year = exp_year
        self.exp_mo_start = exp_mo_start
        self.exp_mo_end = exp_mo_end
        self._add_box()
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

            xxx - Cannot move an empty box

            xxx - Location is not valid

        :param box:
        :param location:
        :return:
        """
        if type(box) == Box:
            self.box = box
        else:
            self.box = Box()
            self.box.id = box
        self.location = location
        self.product = self.box.product
        self.exp_year = self.box.exp_year
        self.exp_mo_start = self.box.exp_month_start
        self.exp_mo_end = self.box.exp_month_end
        self._move_box()
        return self.box

    def box_consume(self, box: Union[Box, int]):
        """
        Consume (e.g. empty) a box.  The box will be marked empty,
        the activity record will be updated, and the box will be returned.

        Requirements:

        *   The box must not be empty when passed in.

        Exception:

            xxx - The box was already empty

        :param box:
        :return:
        """
        self.box = box
        self.location = self.box.location
        self.product = self.box.product
        self.exp_year = self.box.exp_year
        self.exp_mo_start = self.box.exp_month_start
        self.exp_mo_end = self.box.exp_month_end
        self._consume_box()
        return self.box

    def pallet_finish(self, pallet: Union[Pallet, int]):
        """
        Finish the processing of a pallet  of boxes into inventory.  Each
        box of the pallet will be processed.  Nothing will be returned.

        Note - a pallet is still considered  valid even if there are no
        boxes associated with it.

        Requirements:

        *   A valid pallet record or ID

        Exception:

            xxx - An invalid pallet record or ID was passed in

        :param pallet:
        :return:
        """
        if type(pallet) == Pallet:
            self.pallet = pallet
        else:
            self.pallet = Pallet()
        pallet_boxes = PalletBox.objects.all()
        for pallet_box in pallet_boxes:
            self.box = pallet_box.box
            self.location = self.pallet.location
            self.product = pallet_box.product
            self.exp_year = pallet_box.exp_year
            self.exp_mo_start = pallet_box.exp_month_start
            self.exp_mo_end = pallet_box.exp_month_end
            self._add_box()
        return

    def _add_box(self):
        ...
        self.activity.box_fill(self.box.id)
        return

    def _move_box(self):
        ...
        self.activity.box_move(self.box.id)
        return

    def _consume_box(self):
        ...
        self.activity.box_empty(self.box.id)
        return


if __name__ == "__main__":
    box_mgmt = BoxManagementClass()

# EOF
