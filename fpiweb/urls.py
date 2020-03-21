"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
from django.views.generic import TemplateView


from fpiweb.views import \
    AboutView, \
    BoxEditView, \
    BoxEmptyMoveView, \
    BoxScannedView, \
    IndexView, LoginView, ConstraintsListView, \
    ConstraintCreateView, ConstraintUpdateView, ConstraintDeleteView, \
    LogoutView, BoxAddView, BoxDetailsView, \
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

    # Constraint List page
    # e.g. /fpiweb/constraints/ = list of constraints
    path('constraints/', ConstraintsListView.as_view(),
         name='constraints_view'),

    # # e.g. /fpiweb/constraints/4/ = show constraint # 4
    # path('constraint/<int:constraint>', ConstraintDetailView.as_view(),
    #      name='constraint_detail', ),

    # e.g. /fpiweb/constraints/add/ = add a constraint
    path('constraint/add/', ConstraintCreateView.as_view(),
      name='constraint_new', ),

    # e.g. /fpiweb/constraints/edit/4/ = edit constraint # 4
    path('constraint/edit/<int:pk>/', ConstraintUpdateView.as_view(),
        name='constraint_update', ),

    # e.g. /fpiweb/constraints/delete/4/ = delete constraint # 4
    path('constraint/delete/<int:pk>/', ConstraintDeleteView.as_view(),
        name='constraint_delete', ),

    # e.g.  /fpiweb/box/add/ = add a box to inventory
    path('box/add/', BoxAddView.as_view(), name='box_add'),

    # e.g. /fpiweb/box/<pk>/edit = edit a box in inventory
    path('box/<int:pk>/edit/', BoxEditView.as_view(), name='box_edit'),

    # e.g. /fpiweb/box/<pk>/ = view the information about a box
    path('box/<int:pk>/', BoxDetailsView.as_view(), name='box_details'),

    # e.g. /fpiweb/box/box12345/ = view the information about a box
    path('box/box<int:number>/', BoxScannedView.as_view(), name='box_scanned'),

    # e.g. /fpiweb/box/<pk>/empty_move = consume or move a box
    path('box/<int:pk>/empty_move/', BoxEmptyMoveView.as_view(),
         name='box_empty_move'),

    # e.g. /fpiweb/test_scan/ = ???
    path('test_scan/', TestScanView.as_view(), name='test_scan'),
]
