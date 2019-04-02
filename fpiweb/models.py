"""
models.py - Define the database tables using ORM models.
"""

from django.db import models


class BoxType(models.Model):
    """
    Type of box and default quantity.
    """
    BoxTypeID = models.AutoField('Internal Box Type ID', primary_key=True)
    """ Internal record identifier for box type. """
    BoxTypeCode = models.CharField('Box Type Code', max_length=10, unique=True)
    """ Type of box (code or shorthand). """
    BoxTypeDescr = models.CharField('Box Type Description', max_length=30)
    """ Type of box (description). """
    BoxTypeQty = models.IntegerField('Default Box Type Quantity')
    """ Number of items (usually cans) that can typically fix in this box. """

    # define a default display of BoxType
    def __str__(self):
        """ Default way to display this box type record. """
        display = f'{self.BoxTypeCode} - {self.BoxTypeDescr} ' \
            f'({self.BoxTypeQty})'
        return display

    class Meta:
        ordering = ['BoxTypeCode']
        app_label = 'fpiweb'


class ProductCategory(models.Model):
    """
    Category or group of product.
    """
    ProdCatID = models.AutoField('Internal Product Category ID',
                                 primary_key=True)
    """ Internal record identifier for product category. """
    ProdCatName = models.CharField('Product Category Name', max_length=30,
                                   unique=True)
    """ Name of this product category. """
    ProdCatDescr = models.TextField('Product Category Description', null=True)
    """ Description of this product category. """

    # define a default display of Product Category
    def __str__(self):
        """ Default way to display this product category record. """
        display = f'{self.ProdCatName}'
        if self.ProdCatDescr:
            display += f'{self.ProdCatDescr[:50]}'
        return display

    class Meta:
        ordering = ['ProdCatName']
        app_label = 'fpiweb'


class Product(models.Model):
    """
    Product name and attributes.
    """
    ProdID = models.AutoField('Internal Product ID', primary_key=True)
    """ Internal record identifier for product. """
    ProdName = models.CharField('Product Name', max_length=30)
    """ Name of this product. """
    ProdCat = models.ForeignKey(ProductCategory, on_delete=models.PROTECT,
                                verbose_name='Product Category')
    """ Product category associated with this product. """

    # define a default display of Product
    def __str__(self):
        """ Default way to display this Product record. """
        display = f'{self.ProdName} ({self.ProdCat})'
        return display

    class Meta:
        ordering = ['ProdName']
        app_label = 'fpiweb'


class Box(models.Model):
    """
    Box or container for product.
    """
    BoxID = models.AutoField('Internal Box ID', primary_key=True)
    """ Internal record identifier for box. """
    BoxNumber = models.CharField('Visible Box Number', max_length=8,
                                 unique=True)
    """ Number printed in the label on the box. """
    BoxType = models.ForeignKey(BoxType, on_delete=models.PROTECT,
                                verbose_name='Type of Box')
    """ Type of box with this number. """
    LocRow = models.CharField('Row Location', max_length=2, null=True,
                              blank=True)
    """ Row containing this box, if filled. """
    LocBin = models.CharField('Bin Location', max_length=2, null=True,
                              blank=True)
    """ Bin containing this box, if filled. """
    LocTier = models.CharField('Tier Location', max_length=2, null=True,
                               blank=True)
    """ Tier containing this box, if filled. """
    Product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                verbose_name='Product', null=True, blank=True)
    """ Product contained in this box, if filled. """
    ExpirationYear = models.IntegerField('Year Product Expires', null=True,
                                         blank=True)
    """ Year the product expires, if filled. """
    ExpirationMonthStart = models.IntegerField('Expiration Start Month '
                                               '(Optional)', null=True,
                                               blank=True)
    """ 
    Optional starting month range of when the product expires, if filled. 
    """
    ExpirationMonthEnd = models.IntegerField('Expiration End Month '
                                             '(Optional)', null=True,
                                             blank=True)
    """ Optional emding month range of when the product expires, if filled. """
    DateFilled = models.DateTimeField('Date Box Filled', null=True, blank=True)
    """ Approximate date box was filled, if filled."""
    Quantity = models.IntegerField('Quantity in Box', null=True, blank=True)
    """ Approximate or default number of items in the box, if filled. """

    # define a default display of Box
    def __str__(self):
        """ Default way to display this box record. """
        if self.ExpirationMonthStart or self.ExpirationMonthEnd:
            display = f'{self.BoxNumber} ({self.BoxType}) ' \
                f'{self.LocRow}/{self.LocBin}/{self.LocTier} ' \
                f'{self.Product} {self.Quantity}' \
                f'{self.ExpirationYear} ' \
                f'({self.ExpirationMonthStart}-{self.ExpirationMonthEnd})' \
                f'{self.DateFilled}'
        else:
            display = f'{self.BoxNumber} ({self.BoxType}) ' \
                f'{self.LocRow}/{self.LocBin}/{self.LocTier} ' \
                f'{self.Product} {self.Quantity}' \
                f'{self.ExpirationYear} {self.DateFilled}'
        return display

    class Meta:
        ordering = ['BoxNumber']
        app_label = 'fpiweb'


class Activity(models.Model):
    """
    Activity (history) from the past.
    """
    Activity_ID = models.AutoField('Internal Activity ID', primary_key=True)
    """ Internal record identifier for an activity. """
    BoxNumber = models.CharField('Visible Box Number', max_length=8,
                                 unique=True)
    """ Box number on box at time of consumption. """
    BoxTypeCode = models.CharField('Box Type Code', max_length=10)
    """ Box type holding consumed product. """
    LocRow = models.CharField('Row Location', max_length=2)
    """ Rox box was in at the time product was consumed. """
    LocBin = models.CharField('Bin Location', max_length=2)
    """ Bin box was in at the time product was consumed. """
    LocTier = models.CharField('Tier Location', max_length=2)
    """ Tier box was in at the time product was consumed. """
    ProdName = models.CharField('Product Name', max_length=30)
    """ Product contained in box at time of consumption. """
    ProdCatName = models.CharField('Product Category Name', max_length=30)
    """ Category of product consumed. """
    DateFilled = models.DateField('Date Box Filled')
    """ Approximate date product was put in the box. """
    DateConsumed = models.DateField('Date Box Emptied')
    """ Date product was consumed. """
    Duration = models.IntegerField('Duration')
    """ Number of days between date box was filled and consumed."""
    ExpirationYear = models.IntegerField('Year Expired')
    """ Year product would have expired. """
    ExpirationMonthStart = models.IntegerField('Start Expiration Month',
                                               null=True, blank=True)
    """ Optional starting month product would have expired. """
    ExpirationMonthEnd = models.IntegerField('End Expiration Month', null=True,
                                             blank=True)
    """ Optional ending month product would have expired. """
    Quantity = models.IntegerField('Quantity in Box', null=True)
    """ Approximate number of items in the box when it was filled. """

    # define a default display of Activity
    def __str__(self):
        """ Default way to display this activity record. """
        if self.DateFilled:
            display = f'{self.BoxNumber} ({self.BoxTypeCode}) ' \
                f'{self.ProdName} ({self.ProdCatName})' \
                f'{self.Quantity} ' \
                f'{self.ExpirationYear}' \
                f'({self.ExpirationMonthStart}-{self.ExpirationMonthEnd})' \
                f'{self.DateFilled} - {self.DateConsumed} ' \
                f'({self.Duration})' \
                f'at {self.LocRow}/{self.LocBin}/{self.LocTier} '
        else:
            display = f'{self.BoxNumber} ({self.BoxTypeCode}) - Empty'
        return display

    class Meta:
        ordering = ['DateConsumed', ['BoxNumber']]
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

    ConstraintID = models.AutoField('Internal Constraint ID', primary_key=True)
    """ Internal record identifier for a constraint. """
    ConstraintName = models.CharField('Constraint Name', max_length=30)
    """ Coded name of a constraint. """
    ConstraintDescr = models.TextField('Constraint Description', null=True)
    """ Description of a constraint. """
    ConstraintType = models.CharField('Constraint Type', max_length=15,
                                      choices=CONSTRAINT_TYPE_CHOICES)
    """ Type of constraint (integer or character, list or range). """
    ConstraintMin = models.CharField('Minimum Valid Constraint', null=True,
                                     max_length=30, blank=True)
    """ If a range, what is the minimum valid value? """
    ConstraintMax = models.CharField('Maximum Valid Constraint', null=True,
                                     max_length=30, blank=True)
    """ If a range, what is the maximum valid value? """
    ConstraintList = models.CharField('Valid Constraint List', null=True,
                                      max_length=500, blank=True)
    """ If a list, what aew the valid values? """

    # define a default display of Constraints
    def __str__(self):
        """ Default way to display this constraint record. """
        if self.ConstraintType in [self.INT_RANGE, self.CHAR_RANGE]:
            display = f'{self.ConstraintName} - {self.ConstraintMin} to ' \
                f'{self.ConstraintMax} ({self.ConstraintType})'
        else:
            display = f'{self.ConstraintName} - {self.ConstraintList} ' \
                f'({self.ConstraintType})'
        if self.ConstraintDescr:
            display += f' -- {self.ConstraintDescr[:50]}'
        return display

    class Meta:
        ordering = ['ConstraintName']
        app_label = 'fpiweb'

# EOF
