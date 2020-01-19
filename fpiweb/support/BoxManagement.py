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
        Add a new (empty box) to inventory.

        :param box_number: in the form of 'BOXnnnnn'
        :param box_type: a valid box type
        :return: the newly created box record
        """
        self.box = Box()
        self.box.box_number = box_number
        self.box.box_type = box_type
        return self.box

    def box_fill(self, box: Union[Box, Box.id],
                 location: Union[Location, Location.id],
                 product: Union[Product, Product.id], exp_year: int,
                 exp_mo_start: int = 0, exp_mo_end: int = 0
                 ):
        """
        Fill an individual box with product and add to the inventory.

        Requirements:
        *   Box record has not been modified
        *   All required fields be valid
        *   Optional month start and end, if specified, must bracket one or
            more months

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

    def box_move(self, box: Union[Box, Box.id],
                 location: Union[Location, Location.id]
                 ):
        """
        Move an individual box in the inventory.

        See `:doc:Box Management<Box Management>` for intent and details.

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

    def box_consume(self, box: Union[Box, Box.id]):
        """
        Consume (e.g. empty) a box.

        See `:doc:Box Management<Box Management>` for intent and details.

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

    def pallet_finish(self, pallet: Union[Pallet, Pallet.id]):
        """
        Finish the processing of a pallet of boxes into inventory.

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
