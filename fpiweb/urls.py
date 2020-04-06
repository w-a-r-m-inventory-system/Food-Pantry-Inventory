"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
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
    LogoutView, \
    MaintenanceView, \
    ManualBoxMenuView, \
    ManualBoxStatusView, \
    ManualCheckinBoxView, \
    ManualConsumeBoxView, \
    ManualMenuView, \
    ManualMoveBoxView, \
    ManualNewBoxView, \
    ManualPalletMenuView, \
    ManualPalletMoveView, \
    ManualPalletNew, \
    ManualPalletStatus, \
    PalletManagementView, \
    PalletSelectView, \
    PrintLabelsView, \
    ScannerView, \
    TestScanView
# from fpiweb.views import ConstraintDetailView

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

    # Manual box management menu
    # e.g. /fpiweb/manualmenu/ = show manual box management menu
    path(
        'manualmenu/',
        ManualMenuView.as_view(),
        name='manual_menu'
    ),

    # Manual pallet management menu
    # e.g. /fpiweb/manualpalletmenu/ = show manual pallet management menu
    path('manualpalletmenu/',
         ManualPalletMenuView.as_view(),
         name='manual_pallet_menu'),

    # Manual box management menu
    # e.g. /fpiweb/manualboxmenu/ = show manual box management menu
    path('manualboxmenu/',
         ManualBoxMenuView.as_view(),
         name='manual_box_menu'),

    # Manually start a new pallet
    # e.g. /fpiweb/manualpalletnew = manually starting a new pallet
    path(
        'manual_pallet_new/',
        ManualPalletNew.as_view(),
        name='manual_pallet_new'
    ) ,

    path(
        'manual_pallet_move/',
        ManualPalletMoveView.as_view(),
        name='manual_pallet_move',
    ),

    # Manually show the current pallet status
    # e.g. /fpiweb/manualpalletstatus/5/ = current pallet status
    path(
        'manual_pallet_status/<int:pk>',
        ManualPalletStatus.as_view(),
        name='manual_pallet_status'
    ),

    # Manually ask a question or notify user
    # e.g. /fpiweb/manual_note/ = Ask a question or post a note
    # path(
    #     'manual_question/',
    #     ManualNotification.as_view(),
    #     name='manual_question'
    # ),

    path(
        'pallet/management/',
        PalletManagementView.as_view(),
        name='palletManagement',
    ),

    path('build_pallet/', BuildPalletView.as_view(), name='build_pallet'),

    path(
        'build_pallet/<int:box_pk>/',
        BuildPalletView.as_view(),
        name='build_pallet_add_box'),

    path('pallet/select/', PalletSelectView.as_view(), name='pallet_select'),

    path('scanner/', ScannerView.as_view(), name='scanner'),

    path('print_labels/', PrintLabelsView.as_view(), name='print_labels'),

    path(
        'activity/download/',
        ActivityDownloadView.as_view(),
        name='download_activities'),

    # Manually add an empty box to the inventory system
    # e.g. /fpiweb/manual_box_status/ = determine the status of a box manually
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
]
