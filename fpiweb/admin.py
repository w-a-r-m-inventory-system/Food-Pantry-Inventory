"""
Admin.py - Identify what can be mangaged by administrators.
"""

from django.contrib import admin

from .models import BoxType, Box, Activity, Product, ProductCategory, \
    Constraints, ProductExample

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

# Register the models for which we want default admin pages to be built.
admin.site.register(BoxType)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductExample)
admin.site.register(Activity)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'box_number',
        'box_type',
        'loc_row',
        'loc_bin',
        'loc_tier',
        'product',
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


# EOF
