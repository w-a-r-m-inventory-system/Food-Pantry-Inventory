"""
Manage the urls for the F. P. I. application.
"""

from django.urls import path
from django.views.generic import TemplateView


from . import views

# set the namespace for the application
app_name = 'fpiweb'

urlpatterns = [

    # index page
    path('', views.index, name='index'),

    # about page
    path('about/', views.AboutView.as_view()),
    # path('about/', views.AboutView.as_view(template_name='about.html')),

    # index page
    path('index/', views.index, name='index'),

    # about page
    # path('about/', views.AboutView, name='about'),
]
