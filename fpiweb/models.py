"""
models.py - Define the database tables using ORM models.
"""

from django.db import models


class BoxType(models.Model):
    """
    Type of box (Evan's boxes, large boxes, etc.) and default quantity.
    """
    BoxTypeID = models.AutoField('Internal Box Type ID', primary_key=True)
    BoxTypeCode = models.CharField('Box Type Code', max_length=10,
                                   unique=True)
    BoxTypeDescr = models.CharField('Box Type Description', max_length=30)
    BoxTypeQty = models.IntegerField('Default Box Type Quantity')

    # define a default display of BoxType
    def __str__(self):
        display = f'{self.BoxTypeCode} - {self.BoxTypeDescr} ' \
            f'({self.BoxTypeQty})'
        return display


class ProductCategory(models.Model):
    """
    Category or group of product. i.e. Tomato Soup, Canned Pasta, Fruits
    """
    ProdCatID = models.AutoField('Internal Product Category ID',
                                 primary_key=True)
    ProdCatName = models.CharField('Product Category Name',
                                   max_length=30, unique=True)

    # define a default display of Product Category
    def __str__(self):
        display = f'{self.ProdCatName}'
        return display


class Product(models.Model):
    """
    Product name and attributes.  Oranges, Pineapple, Mixed Fruit are products within the Fruits category
    """
    ProdID = models.AutoField('Internal Product ID', primary_key=True)
    ProdName = models.CharField('Product Name', max_length=30)
    ProdCat = models.ForeignKey(ProductCategory, on_delete=models.PROTECT,
                                verbose_name='Product Category')

    # define a default display of Product
    def __str__(self):
        display = f'{self.ProdName} ({self.ProdCat})'
        return display


class Box(models.Model):
    """
    Box or container for product.
    """
    BoxID = models.AutoField('Internal Box ID', primary_key=True)
    BoxNumber = models.CharField('Visible Box Number', max_length=8,
                                 unique=True)
    BoxType = models.ForeignKey(BoxType, on_delete=models.PROTECT,
                                verbose_name='Type of Box')
    LocRow = models.CharField('Row Location', max_length=2, null=True,
                              blank=True)
    LocBin = models.CharField('Bin Location', max_length=2, null=True,
                              blank=True)
    LocTier = models.CharField('Tier Location', max_length=2, null=True,
                               blank=True)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                verbose_name='Product', null=True, blank=True)
    ExpirationYear = models.IntegerField('Year Product Expires', null=True,
                                         blank=True)
    ExpirationMonthStart = models.IntegerField('Expiration Start Month '
                                               '(Optional)', null=True,
                                               blank=True)
    ExpirationMonthEnd = models.IntegerField('Expiration End Month '
                                             '(Optional)', null=True,
                                             blank=True)
    DateFilled = models.DateTimeField('Date Box Filled', null=True, blank=True)
    Quantity = models.IntegerField('Quantity in Box', null=True, blank=True)

    # define a default display of Box
    def __str__(self):
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


class Activity(models.Model):
    Activity_ID = models.AutoField('Internal Activity ID', primary_key=True)
    BoxNumber = models.CharField('Visible Box Number', max_length=8,
                                 unique=True)
    BoxTypeCode = models.CharField('Box Type Code', max_length=10)
    LocRow = models.CharField('Row Location', max_length=2)
    LocBin = models.CharField('Bin Location', max_length=2)
    LocTier = models.CharField('Tier Location', max_length=2)
    ProdName = models.CharField('Product Name', max_length=30)
    ProdCatName = models.CharField('Product Category Name', max_length=30)
    DateFilled = models.DateField('Date Box Filled')
    DateConsumed = models.DateField('Date Box Emptied')
    Duration = models.IntegerField('Duration')
    ExpirationYear = models.IntegerField('Year Expired')
    ExpirationMonthStart = models.IntegerField('Start Expiration Month',
                                               null=True, blank=True)
    ExpirationMonthEnd = models.IntegerField('End Expiration Month',
                                             null=True, blank=True)
    Quantity = models.IntegerField('Quantity in Box', null=True)

    # define a default display of Activity
    def __str__(self):
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

class Constraints (models.Model):
    """
    Constraints of valid values.
    """

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

    ConstraintID = models.AutoField('Internal Constraint ID', primary_key=True)
    ConstraintName = models.CharField('Constraint Name', max_length=30)
    ConstraintType = models.CharField('Constraint Type', max_length=15,
                                      choices=CONSTRAINT_TYPE_CHOICES)
    ConstraintMin = models.CharField('Minimum Valid Constraint', null=True,
                                     max_length=30, blank=True)
    ConstraintMax = models.CharField('Maximum Valid Constraint', null=True,
                                     max_length=30, blank=True)
    ConstraintList = models.CharField('Valid Constraint List', null=True,
                                      max_length=500, blank=True)

    # define a default display of Constraints
    def __str__(self):
        if self.ConstraintType in [self.INT_RANGE, self.CHAR_RANGE]:
            display = f'{self.ConstraintName} - {self.ConstraintMin} to ' \
                f'{self.ConstraintMax} ({self.ConstraintType})'
        else:
            display = f'{self.ConstraintName} - {self.ConstraintList} ' \
                f'({self.ConstraintType})'
        return display

# EOF
