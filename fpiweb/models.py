"""
models.py - Define the database tables using ORM models.
"""
from enum import Enum, unique

# import as to avoid conflict with built-in function compile
from re import compile as re_compile
from re import IGNORECASE

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.urls import reverse

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


class LocRow(models.Model):
    """
    Location Row in warehouse.
    """

    class Meta:
        ordering = ['loc_row']
        app_label = 'fpiweb'
        verbose_name_plural = 'Loc Rows'

    id_help_text = 'Internal record id for location row.'
    id = models.AutoField(
        'Internal Location Row ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for the location row. """

    loc_row_help_text = 'Location row designation'
    loc_row_max_length = 2  # e.g. "01"
    loc_row_min_length = loc_row_max_length
    loc_row = models.CharField(
        'Loc Row',
        max_length=loc_row_max_length,
        unique=True,
        help_text=loc_row_help_text,
    )
    """ Location Row Designation """

    loc_row_descr_help_text = 'Location row description'
    loc_row_descr_max_length = 20  # e.g. "Row 01"
    loc_row_descr = models.CharField(
        'Loc Row Description',
        max_length=loc_row_descr_max_length,
        help_text=loc_row_descr_help_text,
    )
    """ Location Row Description """

    def __str__(self) -> str:
        """ Return just the row for a special form need. """
        return str(self.loc_row)

    def __repr__(self) -> str:
        """ Default way  to display a location row record. """
        display = (
            f'Row {self.loc_row} ({self.loc_row_descr})'
        )
        return display


class LocBin(models.Model):
    """
    Location Bin in warehouse.
    """

    class Meta:
        ordering = ['loc_bin']
        app_label = 'fpiweb'
        verbose_name_plural = 'Loc Bins'

    id_help_text = 'Internal record id for location bin.'
    id = models.AutoField(
        'Internal Location Bin ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for the location bin. """

    loc_bin_help_text = 'Location bin designation'
    loc_bin_max_length = 2
    loc_bin_min_length = loc_bin_max_length
    loc_bin = models.CharField(
        'Loc Bin',
        max_length=loc_bin_max_length,
        unique=True,
        help_text=loc_bin_help_text,
    )
    """ Location Bin Designation """

    loc_bin_descr_help_text = 'Location bin description'
    loc_bin_descr_max_length = 20  # e.g. "Bin 01"
    loc_bin_descr = models.CharField('Loc Bin Description',
        max_length=loc_bin_descr_max_length,
        help_text=loc_bin_descr_help_text,
    )
    """ Location Bin Description """

    def __str__(self) -> str:
        """ Return just the bin for a special form need. """
        return str(self.loc_bin)

    def __repr__(self) -> str:
        """ Default way  to display a location bin record. """
        display = (
            f'Bin {self.loc_bin} ({self.loc_bin_descr})'
        )
        return display


class LocTier(models.Model):
    """
    Location Tier in warehouse.
    """

    class Meta:
        ordering = ['loc_tier']
        app_label = 'fpiweb'
        verbose_name_plural = 'Loc Tiers'

    id_help_text = 'Internal record id for location tier.'
    id = models.AutoField(
        'Internal Location Tier ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for the location tier. """

    loc_tier_help_text = 'Location tier designation'
    loc_tier_max_length = 2
    loc_tier_min_length = loc_tier_max_length
    loc_tier = models.CharField(
        'Loc Tier',
        max_length=loc_tier_max_length,
        unique=True,
        help_text=loc_tier_help_text,
    )
    """ Location Tier Designation """

    loc_tier_descr_help_text = 'Location tier description'
    loc_tier_descr_max_length = 20  # e.g. "Tier 01"
    loc_tier_descr = models.CharField('Loc Tier Description',
        max_length=loc_tier_descr_max_length,
        help_text=loc_tier_descr_help_text, )
    """ Location Tier Description """

    def __str__(self) -> str:
        """ Return just the tier for a special form need. """
        return str(self.loc_tier)

    def __repr__(self) -> str:
        """ Default way  to display a location tier record. """
        display = (
            f'Tier {self.loc_tier} ({self.loc_tier_descr})'
        )
        return display


class Location(models.Model):
    """
    Location for a filled box or other container.
    """

    class Meta:
        ordering = ['loc_code']
        app_label = 'fpiweb'
        verbose_name_plural = 'Locations'

    id_help_text = 'Internal record identifier for location.'
    id = models.AutoField('Internal Location ID', primary_key=True,
        help_text=id_help_text, )
    """ Internal record identifier for location. """

    loc_code_help_text = "Location code"
    loc_code_max_length = 12
    loc_code = models.CharField(
        'Location Code',
        max_length=loc_code_max_length,
        unique=True,
        help_text=loc_code_help_text,
    )
    """ Coded Location. """

    loc_descr_help_text = 'Location description'
    loc_descr_max_length = 25
    loc_descr = models.CharField(
        'Location Description',
        max_length=loc_descr_max_length,
        help_text=loc_descr_help_text,
    )
    """ Location description. """

    loc_row_help_text = 'Loc row'
    loc_row = models.ForeignKey(
        LocRow,
        on_delete=models.PROTECT,
        verbose_name='Row',
        help_text=loc_row_help_text,
    )
    """ Row indicator of this location. """

    loc_bin_help_text = 'Loc bin'
    loc_bin = models.ForeignKey(
        LocBin,
        on_delete=models.PROTECT,
        verbose_name='Bin',
        help_text=loc_bin_help_text,
    )
    """ Bin indicator of this location. """

    loc_tier_help_text = 'Loc tier'
    loc_tier = models.ForeignKey(
        LocTier,
        on_delete=models.PROTECT,
        verbose_name='Tier',
        help_text=loc_tier_help_text,
    )
    """ Tier indicator of this location. """

    loc_in_warehouse_help_text = "In warehouse?"
    loc_in_warehouse = models.BooleanField(
        'In warehouse?',
        default=True,
        help_text=loc_in_warehouse_help_text,
    )
    """ Is this location inside the warehouse? """

    def __str__(self) -> str:
        """ Default way to display a location record. """
        display = (f'Location {self.loc_code} - {self.loc_descr}')
        if self.loc_in_warehouse:
            display += (f' ({self.loc_row}/{self.loc_bin}/{self.loc_tier})')
        return display


class BoxType(models.Model):
    """
    Type of box (Evan's boxes, large boxes, etc.) and default quantity.
    """

    class Meta:
        ordering = ['box_type_code']
        app_label = 'fpiweb'

    id_help_text = 'Internal record identifier for box type.'
    id = models.AutoField(
        'Internal Box Type ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for box type. """

    box_type_code_help_text = 'Type of box (code or shorthand).'
    box_type_code = models.CharField(
        'Box Type Code',
        max_length=10,
        unique=True,
        help_text=box_type_code_help_text,
    )
    """ Type of box (code or shorthand). """

    box_type_descr_help_text = 'Type of box (description).'
    box_type_descr = models.CharField(
        'Box Type Description',
        max_length=30,
        help_text=box_type_descr_help_text,
    )
    """ Type of box (description). """

    box_type_qty_help_text = (
        'Number of items (usually cans) that can typically fix in this box.'
    )
    box_type_qty = models.IntegerField(
        'Default Box Type Quantity',
        help_text=box_type_qty_help_text,
    )
    """ Number of items (usually cans) that can typically fix in this box. """

    # define a default display of box_type
    def __str__(self) -> str:
        """ Default way to display this box type record. """
        display = (f'{self.box_type_code} - {self.box_type_descr} '
                  f'({self.box_type_qty})')
        return display


class ProductCategory(models.Model):
    """
    Category or group of product. i.e. Tomato Soup, Canned Pasta, Fruits
    """

    class Meta:
        ordering = ['prod_cat_name']
        app_label = 'fpiweb'
        verbose_name_plural = 'Product Categories'

    id_help_text = 'Internal record identifier for product category.'
    id = models.AutoField(
        'Internal Product Category ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for product category. """

    prod_cat_name_help_text = 'Name of this product category.'
    prod_cat_name = models.CharField(
        'Product Category Name',
        max_length=30,
        unique=True,
        help_text=prod_cat_name_help_text,
    )
    """ Name of this product category. """

    prod_cat_descr_help_text = 'Description of this product category.'
    prod_cat_descr = models.TextField(
        'Product Category Description',
        null=True,
        help_text=prod_cat_descr_help_text,
    )
    """ Description of this product category. """

    # define a default display of product Category
    def __str__(self):
        """ Default way to display this product category record. """
        display = f'{self.prod_cat_name}'
        if self.prod_cat_descr:
            display += f' - {self.prod_cat_descr[:50]}'
        return display


class Product(models.Model):
    """
    Product name and attributes.  Oranges, Pineapple, Mixed Fruit are products
    within the Fruits category
    """

    class Meta:
        ordering = ['prod_name']
        app_label = 'fpiweb'

    id_help_text = 'Internal record identifier for product.'
    id = models.AutoField(
        'Internal Product ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for product. """

    prod_name_help_text = 'Name of this product.'
    prod_name = models.CharField(
        'product Name',
        max_length=30,
        unique=True,
        help_text=prod_name_help_text,
    )
    """ Name of this product. """

    prod_cat_help_text = 'Product category associated with this product.'
    prod_cat = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        verbose_name='Product Category',
        help_text=prod_cat_help_text,
    )
    """ Product category associated with this product. """

    # define a default display of product
    def __str__(self):
        """ Default way to display this product record. """
        display = f'{self.prod_name} ({self.prod_cat})'
        return display


class BoxNumber:

    # This regex may be used to determine if string is a properly formatted
    # box number.
    box_number_regex = re_compile(r'^BOX\d{5}$')

    # This regex may be used to determine if a string contains a box number.
    # Case is ignored.
    box_number_search_regex = re_compile(r'box\d{5}', IGNORECASE)

    @staticmethod
    def format_box_number(int_box_number: int) -> str:
        """ format an integer into a box number """
        formatted_box_number = "BOX{:05}".format(int_box_number)
        return formatted_box_number

    @staticmethod
    def get_next_box_number() -> str:
        """ get the next unused box number """
        max_box_number = Box.objects.aggregate(
            max_box_number=Max('box_number'))
        max_box_number = max_box_number.get('max_box_number')
        if max_box_number is None:
            max_formatted_box_number = BoxNumber.format_box_number(1)
        else:
            max_box_number = int(max_box_number[3:])
            max_formatted_box_number = \
                BoxNumber.format_box_number(max_box_number + 1)
        return max_formatted_box_number

    @staticmethod
    def validate(box_number: str) -> bool:
        """ validate that a atring is of the form 'BOXnnnnn' """
        is_valid_box_number = \
            bool(BoxNumber.box_number_regex.match(box_number))
        return is_valid_box_number


class BoxError(RuntimeError):
    pass


class Box(models.Model):
    """
    Box or container for product.
    """

    class Meta:
        ordering = ['box_number']
        app_label = 'fpiweb'
        verbose_name_plural = 'Boxes'

    id_help_text = 'Internal record identifier for box.'
    id = models.AutoField(
        'Internal Box ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for box. """

    box_number_help_text = "Number printed in the label on the box."
    box_number_max_length = 8
    box_number_min_length = box_number_max_length
    box_number = models.CharField(
        'Visible Box Number',
        max_length=box_number_max_length,
        unique=True,
        help_text=box_number_help_text,
    )
    """ Number printed in the label on the box. """

    @staticmethod
    def box_type_default():
        box_type = BoxType.objects \
            .filter(box_type_code__istartswith='ev') \
            .first()
        if box_type:
            return box_type
        box_type = BoxType.objects.first()
        if box_type:
            return box_type
        return None

    box_type_help_text = 'Type of box with this number.'
    box_type = models.ForeignKey(
        BoxType,
        on_delete=models.PROTECT,
        verbose_name='Type of Box',
        help_text=box_type_help_text,
    )
    """ Type of box with this number. """

    location = models.ForeignKey(
        "Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Location of Box"
    )

    product_help_text = 'Product contained in this box, if filled.'
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='product',
        null=True,
        blank=True,
        help_text=product_help_text,
    )
    """ Product contained in this box, if filled. """

    exp_year_help_text = 'Year the product expires, if filled.'
    exp_year = models.IntegerField(
        'Year Product Expires',
        null=True,
        blank=True,
        help_text=exp_year_help_text,
    )
    """ Year the product expires, if filled. """

    exp_month_start_help_text = (
        'Optional starting month range of when the product expires, if filled.'
    )
    exp_month_start = models.IntegerField(
        'Expiration Start Month (Optional)',
        null=True,
        blank=True,
        help_text=exp_month_start_help_text
    )
    """
    Optional starting month range of when the product expires, if filled.
    """

    exp_month_end_help_text = (
        'Optional ending month range of when the product expires, if filled.'
    )
    exp_month_end = models.IntegerField(
        'Expiration End Month (Optional)',
        null=True,
        blank=True,
        help_text=exp_month_end_help_text,
    )
    """ Optional emding month range of when the product expires, if filled. """

    date_filled_help_text = 'Approximate date box was filled, if filled.'
    date_filled = models.DateTimeField(
        'Date Box Filled',
        null=True,
        blank=True,
        help_text=date_filled_help_text,
    )
    """ Approximate date box was filled, if filled. """

    quantity_help_text = (
        'Approximate or default number of items in the box, if filled.'
    )
    quantity = models.IntegerField(
        'Quantity in Box',
        null=True,
        blank=True,
        help_text=quantity_help_text,
    )
    """ Approximate or default number of items in the box, if filled. """

    # define a default display of Box
    def __str__(self):
        """ Default way to display this box record. """
        if self.exp_month_start or self.exp_month_end:
            display = (
                f'{self.box_number} ({self.box_type}) '
                f'{self.product} {self.quantity}'
                f'{self.exp_year} '
                f'({self.exp_month_start}-{self.exp_month_end})'
                f'{self.date_filled}'
            )
        else:
            display = (
                f'{self.box_number} ({self.box_type}) '
                f'{self.product} {self.quantity}'
                f'{self.exp_year} {self.date_filled}'
            )
        return display

    def add(self, date_filled=None) -> None:
        if not date_filled:
            date_filled = timezone.now()
        if not self.exp_year:
            raise BoxError(f'exp_year must be set before Box.add is called')
        Activity.objects.create(
            box_number=self.box_number,
            date_filled=date_filled,
            exp_year=self.exp_year,
            duration=0,
            box_type=self.box_type.box_type_code,
        )
        return None

    """
    The following method was added by John C. as a stub.  Travis R. did not 
    realize this when he wrote the support/BoxActivity.py module.  Later, 
    that module could be incorporated into (or called from this models.py 
    module.  That appears to be the more common way to do it.
    """
    def empty(self):

        # TODO: finish creating activity record
        Activity.objects.create(
            box_number=self.box_number,
            box_type=self.box_type,
        )

        # TODO: clear out location and product info

    def get_absolute_url(self):
        return reverse(
            'fpiweb:box_details',
            kwargs={'pk': self.pk},
        )


class Pallet(models.Model):
    """
    Temporary file to build up a list of boxes on a pallet.
    """

    class Meta:
        ordering = ['user']
        app_label = 'fpiweb'
        verbose_name_plural = 'Pallets'

    # Pallet Status Names
    FILL: str = 'Fill'
    MERGE: str = 'Merge'
    MOVE: str = "Move"

    PALLET_STATUS_CHOICES = (
        (FILL, 'Fill pallet for new location'),
        (MERGE, 'Merging boxes on pallet'),
        (MOVE, 'Moving boxes to new location'),
    )

    id_help_text = 'Internal record identifier for a pallet.'
    id = models.AutoField(
        'Internal Pallet ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for a pallet. """

    user_help_text = "User managing this pallet"
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name="User",
        help_text=user_help_text
    )
    """ ID of user building the pallet. """

    location = models.ForeignKey(
        "Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Pallet Location",
    )

    pallet_status_help_text = "Current status of pallet."
    pallet_status = models.CharField(
        'Pallet Status',
        max_length=15,
        choices=PALLET_STATUS_CHOICES,
        help_text=pallet_status_help_text,
    )
    """ Current status of pallet """

    def __str__(self) -> str:
        """ Display the information about this pallet. """
        display = f'Pallet for {self.user} - ' \
                  f'status: {self.pallet_status}'
        return display


class PalletBox(models.Model):
    """
    Temporary file to hold the individual boxes for a pallet.
    """

    class Meta:
        ordering = ''
        app_label = 'fpiweb'
        verbose_name_plural = 'Pallet Boxes'

    # Pallet Box Status Names
    NEW: str = 'New'
    ORIGINAL: str = 'Original'
    MOVE: str = "Move"

    PALLET_BOX_STATUS_CHOICES = (
        (NEW, 'New box added'),
        (ORIGINAL, 'Box already here'),
        (MOVE, 'Box being moved'),
    )

    id_help_text = 'Internal record identifier for a pallet box.'
    id = models.AutoField(
        'Internal Pallet Box ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for a pallet box. """

    pallet_help_text = 'Internal record identifier for a pallet.'
    pallet = models.ForeignKey(
        Pallet,
        on_delete=models.PROTECT,
        help_text=pallet_help_text,
    )

    box_help_text = 'Internal record ideentifier for a box.'
    box = models.ForeignKey(
        Box,
        on_delete=models.PROTECT,
        help_text=box_help_text,
    )

    box_number_help_text = "Number printed in the label on the box."
    box_number_max_length = 8
    box_number_min_length = box_number_max_length
    box_number = models.CharField(
        'Visible Box Number',
        max_length=box_number_max_length,
        unique=True,
        help_text=box_number_help_text,
    )
    """ Number printed in the label on the box. """

    product_help_text = 'Product contained in this box, if filled.'
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='product',
        help_text=product_help_text,
    )
    """ Product contained in this box, if filled. """

    exp_year_help_text = 'Year the product expires, if filled.'
    exp_year = models.IntegerField(
        'Year Product Expires',
        help_text=exp_year_help_text,
    )
    """ Year the product expires, if filled. """

    exp_month_start_help_text = (
        'Optional starting month range of when the product expires, if filled.'
    )
    exp_month_start = models.IntegerField(
        'Expiration Start Month (Optional)',
        null=True,
        blank=True,
        help_text=exp_month_start_help_text
    )
    """
    Optional starting month range of when the product expires, if filled.
    """

    exp_month_end_help_text = (
        'Optional ending month range of when the product expires, if filled.'
    )
    exp_month_end = models.IntegerField(
        'Expiration End Month (Optional)',
        null=True,
        blank=True,
        help_text=exp_month_end_help_text,
    )
    """ Optional emding month range of when the product expires, if filled. """

    box_status_help_text = 'Box on pallet status.'
    box_status = models.CharField(
        'Box Status',
        max_length=15,
        choices=PALLET_BOX_STATUS_CHOICES,
        help_text=box_status_help_text,
    )
    """ Box on pallet status """

    def __str__(self) -> str:
        """ default way to display a pallet box """
        display = f'{self.box_number} ({self.pallet})' \
                  f'contains {self.product} ' \
                  f'({self.exp_year}'
        if self.exp_month_start or self.exp_month_end:
            display += f'/{self.exp_month_start}/{self.exp_month_end}'
        display += f'), status: {self.box_status}'
        return display


class Activity(models.Model):
    """
    Activity (history) from the past.
    """

    class Meta:
        ordering = ['-date_consumed', 'box_number']
        app_label = 'fpiweb'
        verbose_name_plural = 'Activities'

    # Adjustment Reasons
    ADD_EMPTIED: str = 'Add Emptied'
    MOVE_ADDED: str = 'Move Added'
    CONSUME_ADDED: str = 'Consume Added'

    ADJUSTMENT_CODE_CHOICES: list = (
        (ADD_EMPTIED, 'Add emptied previous contents'),
        (MOVE_ADDED, 'Move added box'),
        (CONSUME_ADDED, 'Consume added box'),
    )

    id_help_text = 'Internal record identifier for an activity.'
    id = models.AutoField(
        'Internal Activity ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for an activity. """

    box_number_help_text = 'Box number on box at time of consumption.'
    box_number = models.CharField(
        'Visible Box Number',
        max_length=8,
        help_text=box_number_help_text,
    )
    """ Box number on box at time of consumption. """

    box_type_help_text = 'Box type holding consumed product.'
    box_type = models.CharField(
        'Box Type Code',
        max_length=10,
        help_text=box_type_help_text,
    )
    """ Box type holding consumed product. """

    location = models.ForeignKey(
        "Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Location of Box",
    )

    prod_name_help_text = 'Product contained in box at time of consumption.'
    prod_name = models.CharField(
        'Product Name',
        max_length=30,
        help_text=prod_name_help_text,
    )
    """ Product contained in box at time of consumption. """

    prod_cat_name_help_text = 'Category of product consumed.'
    prod_cat_name = models.CharField(
        'Product Category Name',
        max_length=30,
        help_text=prod_cat_name_help_text,
    )
    """ Category of product consumed. """

    # Do NOT make date_filed a DateTime
    date_filled_help_text = 'Approximate date product was put in the box.'
    date_filled = models.DateField(
        'Date Box Filled',
        help_text=date_filled_help_text,
    )
    """ Approximate date product was put in the box. """

    # Do NOT make date_filed a DateTime
    date_consumed_help_text = 'Date product was consumed.'
    date_consumed = models.DateField(
        'Date Box Emptied',
        null=True,
        blank=True,
        help_text=date_consumed_help_text,
    )
    """ Date product was consumed. """

    exp_year_help_text = 'Year product would have expired.'
    exp_year = models.IntegerField(
        'Year Expired',
        help_text=exp_year_help_text,
    )
    """ Year product would have expired. """

    exp_month_start_help_text = (
        'Optional starting month product would have expired.'
    )
    exp_month_start = models.IntegerField(
        'Start Expiration Month',
        null=True,
        blank=True,
        help_text=exp_month_start_help_text,
    )
    """ Optional starting month product would have expired. """

    exp_month_end_help_text = (
        'Optional ending month product would have expired.'
    )
    exp_month_end = models.IntegerField(
        'End Expiration Month',
        null=True,
        blank=True,
        help_text=exp_month_end_help_text,
    )
    """ Optional ending month product would have expired. """

    quantity_help_text = (
        'Approximate number of items in the box when it was filled.'
        )
    quantity = models.IntegerField(
        'Quantity in Box',
        default=0,
        help_text=quantity_help_text,
    )
    """ Approximate number of items in the box when it was filled. """

    duration_help_text = (
        'Number of days between date box was filled and consumed.'
    )
    duration = models.IntegerField(
        'Duration',
        help_text=duration_help_text,
    )
    """ Number of days between date box was filled and consumed. """

    adjustment_code_help_text = 'Coded reason if this entry was adjusted'
    adjustment_code = models.CharField(
        'Adjustment Code',
        null=True,
        blank=True,
        max_length=15,
        choices=ADJUSTMENT_CODE_CHOICES,
        help_text=adjustment_code_help_text
    )
    """ Coded reason if this entry was adjusted """

    # define a default display of Activity
    def __str__(self):
        """ Default way to display this activity record. """
        display = f'{self.box_number} ({self.box_type})'
        if self.date_filled:
            display = display + (' '
                f'{self.prod_name} ({self.prod_cat_name}) '
                f'{self.quantity} '
                f'{self.exp_year}'
                f'({self.exp_month_start}-'
                f'{self.exp_month_end}) at '
                f'{self.date_filled}'
            )
        if self.date_consumed:
            display = display + (' '
                f'{self.date_consumed}'
                f'({self.duration} days) '
            )
        if self.adjustment_code:
            display = display + (' '
                f'{self.adjustment_code}'
            )

        return display


@unique
class CONSTRAINT_NAME_KEYS(Enum):
    """
    Valid constraint key values with associated names for each key.
    """
    TIER: str = 'Tier'
    ROW: str = 'Row'
    BIN: str = 'Bin'
    EXP_YEAR: str = 'Expiration Year'
    QUANTITY: str = 'Quantity'


class Constraints(models.Model):
    """
    Constraints of valid values.
    """

    class Meta:
        ordering = ['constraint_name']
        app_label = 'fpiweb'
        verbose_name_plural = 'Constraints'

    # Constraint Choice Names
    INT_RANGE = 'Int-MM'
    CHAR_RANGE = 'Char-MM'
    INT_LIST = 'Int-List'
    CHAR_LIST = 'Char-List'

    CONSTRAINT_TYPE_CHOICES = (
        (INT_RANGE, 'Integer Min/Max'),
        (CHAR_RANGE, 'Character Min/Max'),
        (INT_LIST, 'Integer Valid List'),
        (CHAR_LIST, 'Character Valid List'),
    )

    id_help_text = 'Internal record identifier for a constraint.'
    id = models.AutoField(
        'Internal Constraint ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal record identifier for a constraint. """

    constraint_name_help_text = 'Coded name of a constraint.'
    constraint_name = models.CharField(
        'Constraint Name',
        max_length=30,
        unique=True,
        help_text=constraint_name_help_text,
    )
    """ Coded name of a constraint. """

    constraint_descr_help_text = 'Description of this constraint.'
    constraint_descr = models.TextField(
        'Constraint Description',
        null=True,
        help_text=constraint_descr_help_text,
    )
    """ Description of this constraint. """

    constraint_type_help_text = 'Type of constraint (integer or character, ' \
                                'list or range).'
    constraint_type = models.CharField(
        'Constraint Type',
        max_length=15,
        choices=CONSTRAINT_TYPE_CHOICES,
        help_text=constraint_type_help_text,
    )
    """ Type of constraint (integer or character, list or range). """

    constraint_min_help_text = 'If a range, what is the minimum valid value?'
    constraint_min = models.CharField(
        'Minimum Valid Constraint',
        null=True,
        max_length=30,
        blank=True,
        help_text=constraint_min_help_text,
    )
    """ If a range, what is the minimum valid value? """

    constraint_max_help_text = 'If a range, what is the maximum valid value?'
    constraint_max = models.CharField(
        'Maximum Valid Constraint',
        null=True,
        max_length=30,
        blank=True,
        help_text=constraint_max_help_text,
    )
    """ If a range, what is the maximum valid value? """

    constraint_list_help_text = 'If a list, what are the valid values?'
    constraint_list = models.CharField(
        'Valid Constraint List',
        null=True,
        max_length=500,
        blank=True,
        help_text=constraint_list_help_text,
    )
    """ If a list, what are the valid values? """

    # define a default display of Constraints
    def __str__(self):
        """ Default way to display this constraint record. """
        if self.constraint_type in [self.INT_RANGE, self.CHAR_RANGE]:
            display = (
                f'{self.constraint_name} - {self.constraint_min} to '
                f'{self.constraint_max} ({self.constraint_type})'
            )
        else:
            display = (
                f'{self.constraint_name} - {self.constraint_list} '
                f'({self.constraint_type})'
            )
        if self.constraint_descr:
            display += f' -- {self.constraint_descr[:50]}'
        return display

    @staticmethod
    def get_values(constraint_name):
        try:
            constraint = Constraints.objects.get(
                constraint_name__iexact=constraint_name)
        except Constraints.DoesNotExist:
            return None

        if constraint.constraint_type == Constraints.INT_RANGE:
            return [
                int(constraint.constraint_min),
                int(constraint.constraint_max),
            ]

        if constraint.constraint_type == Constraints.CHAR_RANGE:
            return [
                constraint.constraint_min,
                constraint.constraint_max,
            ]

        if constraint.constraint_type == Constraints.INT_LIST:
            if not constraint.constraint_list:
                return []

            values = []
            for piece in constraint.constraint_list.split(','):
                piece = piece.strip()
                values.append(int(piece))
            return values

        if constraint.constraint_type == Constraints.CHAR_LIST:
            if not constraint.constraint_list:
                return []

            values = []
            for piece in constraint.constraint_list.split(','):
                piece = piece.strip()
                values.append(piece)
            return values

        raise ValueError(
            f"Unrecognized constraint_type {constraint.constraint_type}")


class ProductExample(models.Model):
    """
    Examples of items that go into a labeled product.
    """

    class Meta:
        ordering = ['prod_example_name']
        app_label = 'fpiweb'
        verbose_name_plural = 'Product Examples'

    id_help_text = 'Internal record identifier for product example'
    id = models.AutoField(
        'Internal Product Example ID',
        primary_key=True,
        help_text=id_help_text,
    )
    """ Internal reccord identifier for product example"""

    prod_example_name_help_text = 'Name of example product.'
    prod_example_name = models.CharField(
        'Product Example Name',
        max_length=30,
        unique=True,
        help_text=prod_example_name_help_text,
    )
    """Name of example product."""

    product_help_text = 'Product with which this product name is associated.'
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Product',
        help_text=product_help_text,
    )
    """ Product with which this product example is associated. """

    def __str__(self):
        """ Default way to display this product example """
        display = f'{self.prod_example_name} ({self.prod_id})'
        return display


class Profile(models.Model):
    """
    Track more information about the users of our system.
    """

    class Meta:
        app_label = 'fpiweb'

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    """ Internal link to the default Django User table. """

    title_help_text = 'Job title'
    title_max_length = 30
    title = models.CharField(
        'Title',
        max_length=title_max_length,
        null=True,
        blank=True,
        help_text=title_help_text,
    )

    active_location_help_text = (
        "The active location for when user is building a pallet (Location)"
    )
    active_location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=active_location_help_text,
    )

    def __str__(self) -> str:
        """ display profile information """
        display = f'User: {self.user} - {self.title}'
        if self.active_location:
            display += f' pallet for {self.active_location}'
        return display

# EOF
