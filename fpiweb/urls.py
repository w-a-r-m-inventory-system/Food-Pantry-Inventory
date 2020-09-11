"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView


from fpiweb.views import \
    AboutView, \
    ActivityDownloadView, \
    BoxDetailsView, \
    BoxEditView, \
    BoxEmptyMoveView, \
    BoxEmptyView, \
    BoxItemFormView, \
    BoxMoveView, \
    BoxNewView, \
    BoxScannedView, \
    BuildPalletView, \
    ConstraintCreateView, \
    ConstraintDeleteView, \
    ConstraintsListView, \
    ConstraintUpdateView, \
    IndexView, \
    LocBinCreateView, \
    LocBinDeleteView, \
    LocBinListView, \
    LocBinUpdateView, \
    LocRowCreateView, \
    LocRowDeleteView, \
    LocRowListView, \
    LocRowUpdateView, \
    LocTierCreateView, \
    LocTierDeleteView, \
    LocTierListView, \
    LocTierUpdateView, \
    LoginView, \
    ChangePasswordView, \
    ConfirmPasswordChangeView, \
    LogoutView, \
    MaintenanceView, \
    ManualBoxStatusView, \
    ManualCheckinBoxView, \
    ManualConsumeBoxView, \
    ManualMoveBoxView, \
    ManualNewBoxView, \
    ManualPalletMoveView, \
    PrintLabelsView, \
    ProductCategoryCreateView, \
    TestScanView, \
    UserManagementView, \
    UserCreateview, \
    UserUpdateView, ProductCategoryListView, ProductCategoryUpdateView

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

# set the namespace for the application
app_name = 'fpiweb'

urlpatterns = [

    # index page
    # e.g. /fpiweb/ or /fpiweb/index/
    path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),

    # about page
    # e.g. /fpiweb/about/
    path('about/', AboutView.as_view(), name='about'),

    # login page
    # e.g. /fpiweb/login/
    path('login/', LoginView.as_view(), name='login'),

    # change password page
    # e.g. /fpiweb/change_pswd/
    path('change_pswd/', ChangePasswordView.as_view(), name='change_pswd'),

    # confirm password page
    # e.g. /fpiweb/confirm_pswd/
    path(
        'confirm_pswd/',
        ConfirmPasswordChangeView.as_view(),
        name='confirm_pwsd',
    ),

    # logout page
    # e.g. /fpiweb/logout/
    path('logout/', LogoutView.as_view(), name='logout'),

    # Maintenance page
    # e.g. /fpiweb/maintenance/ = list of constraints
    path('maintenance/', MaintenanceView.as_view(),
         name='maintenance'),

    # LocRow List page
    # e.g. /fpiweb/loc_rows/ = list of loc_rows
    path('loc_row/', LocRowListView.as_view(),
         name='loc_row_view'),

    # LocRow Add page
    # e.g. /fpiweb/loc_row/add/ = add a loc_row
    path('loc_row/add/', LocRowCreateView.as_view(),
         name='loc_row_new', ),

    # LocRow Edit page
    # e.g. /fpiweb/loc_row/edit/4/ = edit loc_row # 4
    path('loc_row/edit/<int:pk>/', LocRowUpdateView.as_view(),
         name='loc_row_update', ),

    # LocRow Delete Page
    # e.g. /fpiweb/loc_row/delete/4/ = delete loc_row # 4
    path('loc_row/delete/<int:pk>/', LocRowDeleteView.as_view(),
         name='loc_row_delete', ),

    # LocBin List page
    # e.g. /fpiweb/loc_bins/ = list of loc_bins
    path('loc_bin/', LocBinListView.as_view(),
         name='loc_bin_view'),

    # LocBin Add page
    # e.g. /fpiweb/loc_bin/add/ = add a loc_bin
    path('loc_bin/add/', LocBinCreateView.as_view(),
         name='loc_bin_new', ),

    # LocBin Edit page
    # e.g. /fpiweb/loc_bin/edit/4/ = edit loc_bin # 4
    path('loc_bin/edit/<int:pk>/', LocBinUpdateView.as_view(),
         name='loc_bin_update', ),

    # LocBin Delete Page
    # e.g. /fpiweb/loc_bin/delete/4/ = delete loc_bin # 4
    path('loc_bin/delete/<int:pk>/', LocBinDeleteView.as_view(),
         name='loc_bin_delete', ),

    # LocTier List page
    # e.g. /fpiweb/loc_tiers/ = list of loc_tiers
    path('loc_tier/', LocTierListView.as_view(),
         name='loc_tier_view'),

    # LocTier Add page
    # e.g. /fpiweb/loc_tier/add/ = add a loc_tier
    path('loc_tier/add/', LocTierCreateView.as_view(),
         name='loc_tier_new', ),

    # LocTier Edit page
    # e.g. /fpiweb/loc_tier/edit/4/ = edit loc_tier # 4
    path('loc_tier/edit/<int:pk>/', LocTierUpdateView.as_view(),
         name='loc_tier_update', ),

    # LocTier Delete Page
    # e.g. /fpiweb/loc_tier/delete/4/ = delete loc_tier # 4
    path('loc_tier/delete/<int:pk>/', LocTierDeleteView.as_view(),
         name='loc_tier_delete', ),

    # Constraint List page
    # e.g. /fpiweb/constraints/ = list of constraints
    path('constraints/', ConstraintsListView.as_view(),
         name='constraints_view'),

    # Constraint Add page
    # e.g. /fpiweb/constraint/add/ = add a constraint
    path('constraint/add/', ConstraintCreateView.as_view(),
         name='constraint_new', ),

    # Constraint Edit page
    # e.g. /fpiweb/constraint/edit/4/ = edit constraint # 4
    path('constraint/edit/<int:pk>/', ConstraintUpdateView.as_view(),
         name='constraint_update', ),

    # Constraint Delete Page
    # e.g. /fpiweb/constraint/delete/4/ = delete constraint # 4
    path('constraint/delete/<int:pk>/', ConstraintDeleteView.as_view(),
         name='constraint_delete', ),

    # Box Add page
    # e.g.  /fpiweb/box/add/ = add a box to inventory
    path('box/new/<str:box_number>/', BoxNewView.as_view(), name='box_new'),

    # Box Edit page
    # e.g. /fpiweb/box/<pk>/edit = edit a box in inventory
    path('box/<int:pk>/edit/', BoxEditView.as_view(), name='box_edit'),

    # Box Detail page
    # e.g. /fpiweb/box/<pk>/ = view the information about a box
    path('box/<int:pk>/', BoxDetailsView.as_view(), name='box_details'),

    # Box scan page (QR code scans will start here)
    # e.g. /fpiweb/box/box12345/ = view the information about a box
    path('box/box<int:number>/', BoxScannedView.as_view(), name='box_scanned'),

    # Move or empty a box
    # e.g. /fpiweb/box/<pk>/empty_move = consume or move a box
    path('box/<int:pk>/empty_move/', BoxEmptyMoveView.as_view(),
         name='box_empty_move'),

    # Move a box
    # e.g. /fpiweb/box/<pk>/move/ = change location of box in inventory
    path('box/<int:pk>/move/', BoxMoveView.as_view(), name='box_move'),

    # fill a box
    # e.g. /fpiweb/box/<pk>/fill/ = fill an empy box and put in inventory
    path('box/<int:pk>/fill/', BoxEmptyMoveView.as_view(), name='box_fill'),

    # Empty a box
    # e.g. /fpiweb/box/<pk>/empty = consume the product in a box
    path('box/<int:pk>/empty/', BoxEmptyMoveView.as_view(), name='box_empty'),

    # send scan image or box number to server receive JSON info on box
    path('box/box_form/', BoxItemFormView.as_view(), name='box_form'),

    # e.g. /fpiweb/test_scan/ = ???
    path('test_scan/', TestScanView.as_view(), name='test_scan'),

    # Add a box to a pallet view
    # e.g. /fpiweb/build_pallet/box/box12345/ = add a box to existing pallet
    path(
        'build_pallet/<str:box_number>/',
        BuildPalletView.as_view(),
        {'box_pk': 'pk'},
        name='build_pallet_add_box'
    ),

    # Start a new pallet view
    # e.g. /fpiweb/build_pallet/ = start a new pallet
    path(
        'build_pallet/',
        BuildPalletView.as_view(),
        name='build_pallet'
    ),

    # Move all boxes in one location to a different location
    # e.g. /fpiweb/manual_pallet_move/
    path(
        'manual_pallet_move/',
        ManualPalletMoveView.as_view(),
        name='manual_pallet_move',
    ),

    # build a pallet of boxes and store in a given location
    path('build_pallet/', BuildPalletView.as_view(), name='build_pallet'),

    # generate a pdf of one or more pages of QR code labels to put on boxes
    # e.g. /fpiweb/print_labels/
    path('print_labels/', PrintLabelsView.as_view(), name='print_labels'),

    # Downlaod a csv file containinng all box activity
    # e.g. /fpiweb/activity/download/
    path(
        'activity/download/',
        ActivityDownloadView.as_view(),
        name='download_activities'),

    # Manually add an empty box to the inventory system
    # e.g. /fpiweb/manual_box_status/ = add a box to the system
    path('manual_add_box/', ManualNewBoxView.as_view(),
         name='manual_add_box', ),

    # Manually check in a box
    # e.g. /fpiweb/manual_checkin_box/ = check in a box manually
    path(
        'manual_checkin_box/',
        ManualCheckinBoxView.as_view(),
        name='manual_checkin_box',
    ),

    # Manually check out a box
    # e.g. /fpiweb/manual_checkout_box/ = check out a box manually
    path(
        'manual_checkout_box/',
        ManualConsumeBoxView.as_view(),
        name='manual_checkout_box',
    ),

    # Manually move a filled box
    # e.g. /fpiweb/manual_move_box/ = move a filled box manually
    path(
        'manual_move_box/',
        ManualMoveBoxView.as_view(),
        name='manual_move_box',
    ),

    # Manually get a box status
    # e.g. /fpiweb/manual_box_status/ = determine the status of a box manually
    path(
        'manual_box_status/',
        ManualBoxStatusView.as_view(),
        name='manual_box_status',
    ),

    # Choose a user account to add or modify
    # e.g. /fpiweb/user_mgmt/ = determine the status of a box manually
    path('user_mgmt/', UserManagementView.as_view(),
         name='user_management'),

    # Add a new user account
    # e.g. /fpiweb/user_mgmt/add/ = add a new user
    path('user_mgmt/add/', UserCreateview.as_view(),
         name='user_new'),

    # Edit an existing user
    # e.g. /fpiweb/user_mgmt/edit/5/ = update an existing user
    path('user_mgmt/edit/<int:pk>', UserUpdateView.as_view(),
         name='user_edit'),

    # ProductCategory List page
    # e.g. /fpiweb/product_category/ = list of product_category
    path('product_category/', ProductCategoryListView.as_view(),
         name='product_category_view'),

    # ProductCategory Add page
    # e.g. /fpiweb/product_category/add/ = add a product_category
    path('product_category/add/', ProductCategoryCreateView.as_view(),
         name='product_category_new' ),

    # ProductCategory Edit page
    # e.g. /fpiweb/product_category/edit/4/ = edit product_category # 4
    path('product_category/edit/<int:pk>/', ProductCategoryUpdateView.as_view(),
         name='product_category_update' ),



]

# EOF
