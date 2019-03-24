"""
Admin.py - Identify what can be mangaged by administrators.
"""

from django.contrib import admin

from .models import BoxType, Box, Activity, Product, ProductCategory, \
    Constraints

# Register the models for which we want default admin pages to be built.
admin.site.register(Box)
admin.site.register(BoxType)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Activity)
admin.site.register(Constraints)

# EOF
