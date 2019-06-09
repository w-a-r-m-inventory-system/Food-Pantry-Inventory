"""
models.py - Define the database tables using ORM models.
"""
from enum import Enum, unique

from django.db import models
from django.utils import timezone

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


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

    box_type_qty_help_text = 'Number of items (usually cans) that can ' \
                             'typically fix in this box.'
    box_type_qty = models.IntegerField(
        'Default Box Type Quantity',
        help_text=box_type_qty_help_text,
    )
    """ Number of items (usually cans) that can typically fix in this box. """

    # define a default display of box_type
    def __str__(self):
        """ Default way to display this box type record. """
        display = f'{self.box_type_code} - {self.box_type_descr} ' \
            f'({self.box_type_qty})'
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
    box_number = models.CharField(
        'Visible Box Number',
        max_length=8,
        unique=True,
        help_text=box_number_help_text,
    )
    """ Number printed in the label on the box. """

    box_type_help_text = 'Type of box with this number.'
    box_type = models.ForeignKey(
        BoxType,
        on_delete=models.PROTECT,
        verbose_name='Type of Box',
        help_text=box_type_help_text,
    )
    """ Type of box with this number. """

    loc_row_help_text = 'Row containing this box, if filled.'
    loc_row = models.CharField(
        'Row Location',
        max_length=2,
        null=True,
        blank=True,
        help_text=loc_row_help_text,
    )
    """ Row containing this box, if filled. """

    loc_bin_help_text = 'Bin containing this box, if filled.'
    loc_bin = models.CharField(
        'Bin Location',
        max_length=2,
        null=True,
        blank=True,
        help_text=loc_bin_help_text,
    )
    """ Bin containing this box, if filled. """

    loc_tier_help_text = 'Tier containing this box, if filled.'
    loc_tier = models.CharField(
        'Tier Location',
        max_length=2,
        null=True,
        blank=True,
        help_text=loc_tier_help_text,
    )
    """ Tier containing this box, if filled. """

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

    exp_month_start_help_text = 'Optional starting month range of when the ' \
                                'product expires, if filled.'
    exp_month_start = models.IntegerField(
        'Expiration Start Month (Optional)',
        null=True,
        blank=True,
        help_text=exp_month_start_help_text)
    """ 
    Optional starting month range of when the product expires, if filled. 
    """

    exp_month_end_help_text = 'Optional ending month range of when the ' \
                              'product expires, if filled.'
    exp_month_end = models.IntegerField(
        'Expiration End Month (Optional)',
        null=True,
        blank=True,
        help_text=exp_month_end_help_text)
    """ Optional emding month range of when the product expires, if filled. """

    date_filled_help_text = 'Approximate date box was filled, if filled.'
    date_filled = models.DateTimeField(
        'Date Box Filled',
        null=True,
        blank=True,
        help_text=date_filled_help_text,
    )
    """ Approximate date box was filled, if filled. """

    quantity_help_text = 'Approximate or default number of items in the ' \
                         'box, if filled.'
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
            display = f'{self.box_number} ({self.box_type}) ' \
                f'{self.loc_row}/{self.loc_bin}/{self.loc_tier} ' \
                f'{self.product} {self.quantity}' \
                f'{self.exp_year} ' \
                f'({self.exp_month_start}-{self.exp_month_end})' \
                f'{self.date_filled}'
        else:
            display = f'{self.box_number} ({self.box_type}) ' \
                f'{self.loc_row}/{self.loc_bin}/{self.loc_tier} ' \
                f'{self.product} {self.quantity}' \
                f'{self.exp_year} {self.date_filled}'
        return display

    def empty(self):

        # TODO: finish creating activity record
        Activity.objects.create(
            box_number=self.box_number,
            box_type=self.box_type,

        )

        # TODO: clear out location and product info


class Activity(models.Model):
    """
    Activity (history) from the past.
    """

    class Meta:
        ordering = ['-date_consumed', 'box_number']
        app_label = 'fpiweb'
        verbose_name_plural = 'Activities'

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

    loc_row_help_text = 'Row box was in at the time product was consumed.'
    loc_row = models.CharField(
        'Row Location',
        max_length=2,
        help_text=loc_row_help_text,
    )
    """ Row box was in at the time product was consumed. """

    loc_bin_help_text = 'Bin box was in at the time product was consumed.'
    loc_bin = models.CharField(
        'Bin Location',
        max_length=2,
        help_text=loc_bin_help_text,
    )
    """ Bin box was in at the time product was consumed. """

    loc_tier_help_text = 'Tier box was in at the time product was consumed.'
    loc_tier = models.CharField(
        'Tier Location',
        max_length=2,
        help_text=loc_tier_help_text,
    )
    """ Tier box was in at the time product was consumed. """

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

    date_filled_help_text = 'Approximate date product was put in the box.'
    date_filled = models.DateField(
        'Date Box Filled',
        help_text=date_filled_help_text,
    )
    """ Approximate date product was put in the box. """

    date_consumed_help_text = 'Date product was consumed.'
    date_consumed = models.DateField(
        'Date Box Emptied',
        help_text=date_consumed_help_text,
    )
    """ Date product was consumed. """

    duration_help_text = 'Number of days between date box was filled and ' \
                         'consumed.'
    duration = models.IntegerField(
        'Duration',
        help_text=duration_help_text,
    )
    """ Number of days between date box was filled and consumed. """

    exp_year_help_text = 'Year product would have expired.'
    exp_year = models.IntegerField(
        'Year Expired',
        help_text=exp_year_help_text,
    )
    """ Year product would have expired. """

    exp_month_start_help_text = \
        'Optional starting month product would have expired.'
    exp_month_start = models.IntegerField(
        'Start Expiration Month',
        null=True,
        blank=True,
        help_text=exp_month_start_help_text,
    )
    """ Optional starting month product would have expired. """

    exp_month_end_help_text = \
        'Optional ending month product would have expired.'
    exp_month_end = models.IntegerField(
        'End Expiration Month',
        null=True,
        blank=True,
        help_text=exp_month_end_help_text,
    )
    """ Optional ending month product would have expired. """

    quantity_help_text = 'Approximate number of items in the box when it ' \
                         'was filled.'
    quantity = models.IntegerField(
        'Quantity in Box',
        default=0,
        help_text=quantity_help_text,
    )
    """ Approximate number of items in the box when it was filled. """

    # define a default display of Activity
    def __str__(self):
        """ Default way to display this activity record. """
        if self.date_filled:
            display = f'{self.box_number} ({self.box_type}) ' \
                f'{self.prod_name} ({self.prod_cat_name}) ' \
                f'{self.quantity} ' \
                f'{self.exp_year}' \
                f'({self.exp_month_start}-' \
                f'{self.exp_month_end})' \
                f'{self.date_filled} - {self.date_consumed}' \
                f'({self.duration}) at ' \
                f'{self.loc_row} / ' \
                f'{self.loc_bin} / ' \
                f'{self.loc_tier}'
        else:
            display = f'{self.box_number} ({self.box_type}) - Empty'
        return display


@unique
class CONSTRAINT_NAME_KEYS(Enum):
    """
    Valid constraint key values with associated names for each key.
    """
    TIER: 'Tier'
    ROW: 'Row'
    BIN: 'Bin'
    EXP_YEAR: 'Expiration Year'
    QUANTITY: 'Quantity'


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
            display = f'{self.constraint_name} - {self.constraint_min} to ' \
                f'{self.constraint_max} ({self.constraint_type})'
        else:
            display = f'{self.constraint_name} - {self.constraint_list} ' \
                f'({self.constraint_type})'
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

    id_help_text = 'Internal reccord identifier for product example'
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

    prod_id_help_text = 'Product with which this product name is associated.'
    prod_id = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Product',
        help_text=prod_id_help_text,
    )
    """ Product with which this product name is associated. """

    def __str__(self):
        """ Default way to display this product example """
        display = f'{self.prod_example_name} ({self.prod_id})'
        return display

# EOF
