"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
from django.views.generic import TemplateView


from fpiweb.views import index, ConstraintsListView, AboutView, LoginView,\
    ConstraintCreateView, ConstraintUpdateView, \
    ConstraintDeleteView
# from fpiweb.views import ConstraintDetailView

# set the namespace for the application
app_name = 'fpiweb'

urlpatterns = [

    # index page
    # e.g. /fpiweb/ or /fpiweb/index/
    path('', index, name='index'),
    path('index/', index, name='index'),

    # about page
    # e.g. /fpiweb/about/
    path('about/', AboutView.as_view(), name='about'),

    # login page
    # e.g. /fpiweb/login/
    path('login/', LoginView.as_view(), name='login'),

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
    path('constraint/edit/<int:pk>', ConstraintUpdateView.as_view(),
        name='constraint_update', ),

    # # e.g. /fpiweb/constraints/delete/4/ = delete constraint # 4
    path('constraint/delete/<int:pk>', ConstraintDeleteView.as_view(),
        name='constraint_delete', ),

]
