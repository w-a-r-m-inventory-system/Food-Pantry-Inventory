"""
models.py - Define the database tables using ORM models.
"""

from django.db import models

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


class BoxType(models.Model):
    """
    Type of box (Evan's boxes, large boxes, etc.) and default quantity.
    """
    id = models.AutoField('Internal Box Type ID', primary_key=True)
    """ Internal record identifier for box type. """
    box_type_code = models.CharField('Box Type Code', max_length=10, unique=True)
    """ Type of box (code or shorthand). """
    box_type_descr = models.CharField('Box Type Description', max_length=30)
    """ Type of box (description). """
    box_type_qty = models.IntegerField('Default Box Type Quantity')
    """ Number of items (usually cans) that can typically fix in this box. """

    # define a default display of box_type
    def __str__(self):
        """ Default way to display this box type record. """
        display = f'{self.box_type_code} - {self.box_type_descr} ' \
            f'({self.box_type_qty})'
        return display

    class Meta:
        ordering = ['box_type_code']
        app_label = 'fpiweb'


class ProductCategory(models.Model):
    """
    Category or group of product. i.e. Tomato Soup, Canned Pasta, Fruits
    """
    id = models.AutoField('Internal Product Category ID',
                                   primary_key=True)
    """ Internal record identifier for product category. """
    prod_cat_name = models.CharField('Product Category Name', max_length=30,
                                     unique=True)
    """ Name of this product category. """
    prod_cat_descr = models.TextField('Product Category Description',
                                      null=True)
    """ Description of this product category. """

    # define a default display of product Category
    def __str__(self):
        """ Default way to display this product category record. """
        display = f'{self.prod_cat_name}'
        if self.prod_cat_descr:
            display += f'{self.prod_cat_descr[:50]}'
        return display

    class Meta:
        ordering = ['prod_cat_name']
        app_label = 'fpiweb'


class Product(models.Model):
    """
    Product name and attributes.  Oranges, Pineapple, Mixed Fruit are products
    within the Fruits category
    """
    id = models.AutoField('Internal Product ID', primary_key=True)
    """ Internal record identifier for product. """
    prod_name = models.CharField('product Name', max_length=30)
    """ Name of this product. """
    prod_cat = models.ForeignKey(ProductCategory, on_delete=models.PROTECT,
                                 verbose_name='Product Category')
    """ Product category associated with this product. """

    # define a default display of product
    def __str__(self):
        """ Default way to display this product record. """
        display = f'{self.prod_name} ({self.prod_cat})'
        return display

    class Meta:
        ordering = ['prod_name']
        app_label = 'fpiweb'


class Box(models.Model):
    """
    Box or container for product.
    """
    id = models.AutoField('Internal Box ID', primary_key=True)
    """ Internal record identifier for box. """
    box_number = models.CharField('Visible Box Number', max_length=8,
                                  unique=True)
    """ Number printed in the label on the box. """
    box_type = models.ForeignKey(BoxType, on_delete=models.PROTECT,
                                 verbose_name='Type of Box')
    """ Type of box with this number. """
    loc_row = models.CharField('Row Location', max_length=2, null=True,
                               blank=True)
    """ Row containing this box, if filled. """
    loc_bin = models.CharField('Bin Location', max_length=2, null=True,
                               blank=True)
    """ Bin containing this box, if filled. """
    loc_tier = models.CharField('Tier Location', max_length=2, null=True,
                                blank=True)
    """ Tier containing this box, if filled. """
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                verbose_name='product', null=True, blank=True)
    """ Product contained in this box, if filled. """
    exp_year = models.IntegerField('Year Product Expires', null=True,
                                   blank=True)
    """ Year the product expires, if filled. """
    exp_month_start = models.IntegerField('Expiration Start Month '
                                               '(Optional)', null=True,
                                          blank=True)
    """ 
    Optional starting month range of when the product expires, if filled. 
    """
    exp_month_end = models.IntegerField('Expiration End Month '
                                             '(Optional)', null=True,
                                        blank=True)
    """ Optional emding month range of when the product expires, if filled. """
    date_filled = models.DateTimeField('Date Box Filled', null=True, blank=True)
    """ Approximate date box was filled, if filled."""
    quantity = models.IntegerField('Quantity in Box', null=True, blank=True)
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

    class Meta:
        ordering = ['box_number']
        app_label = 'fpiweb'


class Activity(models.Model):
    """
    Activity (history) from the past.
    """
    id = models.AutoField('Internal Activity ID', primary_key=True)
    """ Internal record identifier for an activity. """
    box_number = models.CharField('Visible Box Number', max_length=8,
                                  unique=True)
    """ Box number on box at time of consumption. """
    box_type_code = models.CharField('Box Type Code', max_length=10)
    """ Box type holding consumed product. """
    loc_row = models.CharField('Row Location', max_length=2)
    """ Rox box was in at the time product was consumed. """
    loc_bin = models.CharField('Bin Location', max_length=2)
    """ Bin box was in at the time product was consumed. """
    loc_tier = models.CharField('Tier Location', max_length=2)
    """ Tier box was in at the time product was consumed. """
    prod_name = models.CharField('Product Name', max_length=30)
    """ Product contained in box at time of consumption. """
    prod_cat_name = models.CharField('Product Category Name', max_length=30)
    """ Category of product consumed. """
    date_filled = models.DateField('Date Box Filled')
    """ Approximate date product was put in the box. """
    date_consumed = models.DateField('Date Box Emptied')
    """ Date product was consumed. """
    duration = models.IntegerField('Duration')
    """ Number of days between date box was filled and consumed."""
    expiration_year = models.IntegerField('Year Expired')
    """ Year product would have expired. """
    expiration_month_start = models.IntegerField('Start Expiration Month',
                                                 null=True, blank=True)
    """ Optional starting month product would have expired. """
    expiration_month_end = models.IntegerField('End Expiration Month', null=True,
                                               blank=True)
    """ Optional ending month product would have expired. """
    quantity = models.IntegerField('Quantity in Box', null=True)
    """ Approximate number of items in the box when it was filled. """

    # define a default display of Activity
    def __str__(self):
        """ Default way to display this activity record. """
        if self.date_filled:
            display = f'{self.box_number} ({self.box_type_code}) ' \
                f'{self.prod_name} ({self.prod_cat_name})' \
                f'{self.quantity} ' \
                f'{self.expiration_year}' \
                f'({self.expiration_month_start}-{self.expiration_month_end})' \
                f'{self.date_filled} - {self.date_consumed} ' \
                f'({self.duration})' \
                f'at {self.loc_row}/{self.loc_bin}/{self.loc_tier} '
        else:
            display = f'{self.box_number} ({self.box_type_code}) - Empty'
        return display

    class Meta:
        ordering = ['date_consumed', ['box_number']]
        app_label = 'fpiweb'


class Constraints(models.Model):
    """
    Constraints of valid values.
    """

    # Constraint Choice Names
    INT_RANGE = 'Int-MM'
    CHAR_RANGE = 'Char-MM'
    INT_LIST = 'Int-List'
    CHAR_LIST = 'Char-List'

    CONSTRAINT_TYPE_CHOICES = (
        (INT_RANGE, 'Integer Min/Max'), (CHAR_RANGE, 'Character Min/Max'),
        (INT_LIST, 'Integer Valid List'), (CHAR_LIST, 'Character Valid List'),)

    id = models.AutoField('Internal Constraint ID', primary_key=True)
    """ Internal record identifier for a constraint. """
    constraint_name = models.CharField('Constraint Name', max_length=30)
    """ Coded name of a constraint. """
    constraint_descr = models.TextField('Constraint Description', null=True)
    """ Description of a constraint. """
    constraint_type = models.CharField('Constraint Type', max_length=15,
                                       choices=CONSTRAINT_TYPE_CHOICES)
    """ Type of constraint (integer or character, list or range). """
    constraint_min = models.CharField('Minimum Valid Constraint', null=True,
                                      max_length=30, blank=True)
    """ If a range, what is the minimum valid value? """
    constraint_max = models.CharField('Maximum Valid Constraint', null=True,
                                      max_length=30, blank=True)
    """ If a range, what is the maximum valid value? """
    constraint_list = models.CharField('Valid Constraint List', null=True,
                                       max_length=500, blank=True)
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

    class Meta:
        ordering = ['constraint_name']
        app_label = 'fpiweb'

# EOF
