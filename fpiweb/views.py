"""
views.py - establish the views (pages) for the F. P. I. web application.
"""

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy

from fpiweb.forms import LoginForm


def index(request):
    """
    Build index.html web page.

    :param request:
    :return:
    """

    response = HttpResponse("Hello world from Food Pantry Inventory.")
    return response


class LoginView(FormView):
    template_name = 'fpiweb/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if user is None:
            form.add_error(None, "Invalid username and/or password")
            return self.form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)



# EOF
