"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
from django.views.generic import TemplateView


from fpiweb.views import AboutView, ConstraintsListView, index, \
    ConstraintDetailView, ConstraintCreateView, ConstraintUpdateView, \
    ConstraintDeleteView

# set the namespace for the application
app_name = 'fpiweb'

urlpatterns = [

    # index page
    path('', index, name='index'),
    path('index/', index, name='index'),

    # about page
    path('about/', AboutView.as_view, name='about_view'),
    # path('about/', views.AboutView.as_view(template_name='about.html')),

    # about page
    # path('about/', views.AboutView, name='about'),

    # Constraint List page
    # e.g. /fpiweb/constraints/ = list of constraints
    path('constraints/', ConstraintsListView.as_view(),
         name='constraints_view'),

    # e.g. /fpiweb/constraints/4/ = show constraint # 4
    path('constraint/<int:constraint>', ConstraintDetailView.as_view(),
         name='constraint_detail', ),

    # e.g. /fpiweb/constraints/add/ = add a constraint
    path('constraint/add/', ConstraintCreateView.as_view(),
      name='constraint_new', ),

    # e.g. /fpiweb/constraints/edit/4/ = edit constraint # 4
    path('constraint/edit/<int:constraint>', ConstraintUpdateView.as_view(),
        name='constraint_update', ),

    # # e.g. /fpiweb/constraints/delete/4/ = delete constraint # 4
    path('constraint/delete/<int:constraint>', ConstraintDeleteView.as_view(),
        name='constraint_delete', ),

]
