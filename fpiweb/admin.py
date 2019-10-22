"""
Admin.py - Identify what can be mangaged by administrators.
"""

from django.contrib import admin

from .models import \
    Activity, \
    Box, \
    BoxType, \
    Constraints, \
    Location, \
    LocBin, \
    LocRow, \
    LocTier, \
    Product, \
    ProductCategory, \
    ProductExample

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

# Register the models for which we want default admin pages to be built.
admin.site.register(Activity)
admin.site.register(BoxType)
admin.site.register(ProductCategory)
admin.site.register(ProductExample)
admin.site.register(Location)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'box_number',
        'box_type',
        'loc_row',
        'loc_bin',
        'loc_tier',
        'quantity',
        'product',
    )
    list_filter = ('box_type', )


@admin.register(Constraints)
class ConstraintsAdmin(admin.ModelAdmin):
    list_display = (
        'constraint_name',
        'constraint_type',
        'constraint_min',
        'constraint_max',
        'constraint_list',
    )


@admin.register(LocBin)
class LocBinAdmin(admin.ModelAdmin):
    list_display = ('loc_bin', 'loc_bin_descr')


@admin.register(LocRow)
class LocRowAdmin(admin.ModelAdmin):
    list_display = ('loc_row', 'loc_row_descr')


@admin.register(LocTier)
class LocTierAdmin(admin.ModelAdmin):
    list_display = ('loc_tier', 'loc_tier_descr')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'prod_name',
        'prod_cat',
    )


# EOF
