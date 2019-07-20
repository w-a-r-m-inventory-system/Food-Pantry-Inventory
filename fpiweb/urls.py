"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
from django.views.generic import TemplateView


from fpiweb.views import \
    AboutView, \
    BoxEditView, \
    BoxEmptyView, \
    BoxEmptyMoveView, \
    BoxMoveView, \
    BoxScannedView, \
    BuildPalletView, \
    IndexView, \
    LoginView, \
    ConstraintsListView, \
    ConstraintCreateView, \
    ConstraintUpdateView, \
    ConstraintDeleteView, \
    LogoutView, \
    BoxNewView, \
    BoxDetailsView, \
    TestScanView, \
    MaintenanceView, \
    LocBinListView, \
    LocBinCreateView, \
    LocBinUpdateView, \
    LocBinDeleteView

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

    #Box Detail page
    # e.g. /fpiweb/box/<pk>/ = view the information about a box
    path('box/<int:pk>/', BoxDetailsView.as_view(), name='box_details'),

    # Box scan page (QR code scans will start here)
    # e.g. /fpiweb/box/box12345/ = view the information about a box
    path('box/box<int:number>/', BoxScannedView.as_view(), name='box_scanned'),

    # e.g. /fpiweb/box/<pk>/empty_move = consume or move a box
    path('box/<int:pk>/empty_move/', BoxEmptyMoveView.as_view(),
         name='box_empty_move'),

    # e.g. /fpiweb/box/<pk>/move/ = change location of box in inventory
    path('box/<int:pk>/move/', BoxEmptyMoveView.as_view(), name='box_move'),
    # e.g. /fpiweb/box/<pk>/empty_move = consume or move a box
    path('box/<int:pk>/empty_move/', BoxEmptyMoveView.as_view(),
         name='box_empty_move'),

    # e.g. /fpiweb/box/<pk>/fill/ = fill an empy box and put in inventory
    path('box/<int:pk>/fill/', BoxEmptyMoveView.as_view(), name='box_fill'),

    # e.g. /fpiweb/box/<pk>/empty = consume the product in a box
    path('box/<int:pk>/empty/', BoxEmptyMoveView.as_view(), name='box_empty'),

    # e.g. /fpiweb/test_scan/ = ???
    path('box/<int:pk>/move/', BoxMoveView.as_view(), name='box_move'),

    path('box/<int:pk>/empty/', BoxEmptyView.as_view(), name='box_empty'),

    # e.g. /fpiweb/box/<pk>/move/ = change location of box in inventory
    path('box/<int:pk>/move/', BoxEmptyMoveView.as_view(), name='box_move'),
    # e.g. /fpiweb/box/<pk>/empty_move = consume or move a box
    path('box/<int:pk>/empty_move/', BoxEmptyMoveView.as_view(),
         name='box_empty_move'),

    # e.g. /fpiweb/box/<pk>/fill/ = fill an empy box and put in inventory
    path('box/<int:pk>/fill/', BoxEmptyMoveView.as_view(), name='box_fill'),

    # e.g. /fpiweb/box/<pk>/empty = consume the product in a box
    path('box/<int:pk>/empty/', BoxEmptyMoveView.as_view(), name='box_empty'),

    # e.g. /fpiweb/test_scan/ = ???
    path('test_scan/', TestScanView.as_view(), name='test_scan'),

    path(
        'build_pallet/<int:box_pk>/',
        BuildPalletView.as_view(),
        name='build_pallet_add_box'
    ),

    path(
        'build_pallet/<int:box_pk>/',
        BuildPalletView.as_view(),
        name='build_pallet_add_box')
]
