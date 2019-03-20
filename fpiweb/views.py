"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    """
    Build index.html web page.

    :param request:
    :return:
    """

    response = HttpResponse("Hello world from Food Pantry Inventory.")
    return response

# EOF
