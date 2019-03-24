"""
models.py - Define the database tables using ORM models.
"""

from django.db import models


class BoxType(models.Model):
    """
    Type of box and default quantity.
    """
    BoxTypeID = models.AutoField('Internal Box Type ID', primary_key=True)
    BoxTypeCode = models.CharField('Box Type Code', max_length=10,
                                   unique=True)
    BoxTypeDescr = models.CharField('Box Type Description', max_length=30)
    BoxTypeQty = models.IntegerField('Default Box Type Quantity')


class ProductCategory(models.Model):
    """
    Category or group of product.
    """
    ProdCatID = models.AutoField('Internal Product Category ID',
                                 primary_key=True)
    ProdCatName = models.CharField('Product Category Name',
                                   max_length=30, unique=True)


class Product(models.Model):
    """
    Product name and attributes.
    """
    ProdID = models.AutoField('Internal Product ID', primary_key=True)
    ProdName = models.CharField('Product Name', max_length=30)
    ProdCat = models.ForeignKey(ProductCategory, on_delete=models.PROTECT,
                                verbose_name='Product Category')


class Box(models.Model):
    """
    Box or container for product.
    """
    BoxID = models.AutoField('Internal Box ID', primary_key=True)
    BoxNumber = models.CharField('Visible Box Number', max_length=8,
                                 unique=True)
    BoxType = models.ForeignKey(BoxType, on_delete=models.PROTECT,
                                verbose_name='Type of Box')
    LocRow = models.CharField('Row Location', max_length=2, null=True)
    LocBin = models.CharField('Bin Location', max_length=2, null=True)
    LocTier = models.CharField('Tier Location', max_length=2, null=True)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                verbose_name='Product', null=True)
    ExpirationYear = models.IntegerField('Year Product Expires', null=True)
    ExpirationMonthStart = models.IntegerField('Expiration Start Month '
                                               '(Optional)', null=True)
    ExpirationMonthEnd = models.IntegerField('Expiration End Month '
                                             '(Optional)', null=True)
    DateFilled = models.DateTimeField('Date Box Filled', null=True)
    Quantity = models.IntegerField('Quantity in Box', null=True)


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
    ExpirationYear = models.IntegerField('Year Expired')
    ExpirationMonthStart = models.IntegerField('Start Expiration Month',
                                               null=True)
    ExpirationMonthEnd = models.IntegerField('End Expiration Month',
                                             null=True)
    Quantity = models.IntegerField('Quantity in Box', null=True)


CONSTRAINT_TYPE_CHOICES = (
    ('Int-MM', 'Integer Min/Max'),
    ('Char-MM', 'Character Min/Max'),
    ('Int-List', 'Integer Valid List'),
    ('Char-List', 'Character Valid List'),
)

class Constraints (models.Model):
    """
    Constraints of valid values.
    """
    ConstraintID = models.AutoField('Internal Constraint ID', primary_key=True)
    ConstraintName = models.CharField('Constraint Name', max_length=30)
    ConstraintType = models.CharField('Constraint Type', max_length=15,
                                      choices=CONSTRAINT_TYPE_CHOICES)
    ConstraintMin = models.CharField('Minimum Valid Constraint', null=True,
                                     max_length=30)
    ConstraintMax = models.CharField('Maximum Valid Constraint', null=True,
                                     max_length=30)
    ConstraintList = models.CharField('Valid Constraint List', null=True,
                                      max_length=500)

# EOF
