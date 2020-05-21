"""
Admin.py - Identify what can be managed by administrators.
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
    Pallet, \
    PalletBox, \
    Product, \
    ProductCategory, \
    ProductExample, \
    Pallet, \
    PalletBox, \
    Profile

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


# Register the models for which we want default admin pages to be built.
admin.site.register(ProductCategory)
admin.site.register(ProductExample)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'box_number',
        'date_filled',
        'date_consumed',
        'adjustment_code',
    )
    list_filter = (
        'adjustment_code',
    )


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'box_number',
        'box_type',
        'location',
        'quantity',
        'product',
    )
    list_filter = ('box_type', )


@admin.register(BoxType)
class BoxTypeAdmin(admin.ModelAdmin):
    list_display = (
        'box_type_code',
        'box_type_descr',
        'box_type_qty',
    )


@admin.register(Constraints)
class ConstraintsAdmin(admin.ModelAdmin):
    list_display = (
        'constraint_name',
        'constraint_type',
        'constraint_min',
        'constraint_max',
        'constraint_list',
    )


@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = (
        'pk',
        'loc_row',
        'loc_bin',
        'loc_tier',
    )
    list_filter = (
        'loc_row',
        'loc_bin',
        'loc_tier',
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


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(PalletBox)
class PalletBoxAdmin(admin.ModelAdmin):
    list_display = (
        'box_number',
        'pallet',
        'box',
        'product',
        'exp_year',
        'exp_month_start',
        'exp_month_end'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'prod_name',
        'prod_cat',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'active_pallet_id',
    )

# EOF
