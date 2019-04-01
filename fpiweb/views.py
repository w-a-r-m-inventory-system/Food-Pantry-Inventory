"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

from fpiweb.models import Constraints


def index(request):
    """
    Build index.html web page.

    :param request:
    :return:
    """

    response = HttpResponse("Hello world from Food Pantry Inventory.")
    return response


class AboutView(TemplateView):
    """
    The About View for this application.
    """
    template_name = 'fpiweb/about.html'

# EOF
