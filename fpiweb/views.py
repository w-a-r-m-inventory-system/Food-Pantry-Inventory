"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView, FormView

from fpiweb.forms import LoginForm, ConstraintsForm, LogoutForm
from fpiweb.models import Constraints

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


class IndexView(TemplateView):
    """
    Default web page (/index)
    """
    template_name = 'fpiweb/index.html'


class AboutView(TemplateView):
    """
    The About View for this application.
    """
    template_name = 'fpiweb/about.html'
    mycontext = dict()
    mycontext['project_type'] = 'open source'
    extra_context = mycontext


class LoginView(FormView):
    template_name = 'fpiweb/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('fpiweb:index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user is None:
            form.add_error(None, "Invalid username and/or password")
            return self.form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)


class LogoutView(TemplateView):
    template_name = 'fpiweb/logout.html'
    form_class = LogoutForm
    success_url = reverse_lazy('fpiweb:index')

    def form_valid(self, form):

        logout(self.request)
        return super().form_valid(form)


class ConstraintsListView(LoginRequiredMixin, ListView):
    """
    List of existing constraints.
    """
    model = Constraints
    template_name = 'fpiweb/constraints_list.html'
    context_object_name = 'constraints_list_content'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Add additional content to the context dictionary.

        :param object_list:
        :param kwargs:
        :return:
        """
        context = super(ConstraintsListView, self).get_context_data()

        # provide additional information to the template
        INT_RANGE = Constraints.INT_RANGE
        CHAR_RANGE = Constraints.CHAR_RANGE
        range_list = [INT_RANGE, CHAR_RANGE]
        context['range_list'] = range_list

        return context


class ConstraintCreateView(LoginRequiredMixin, CreateView):
    """
    Create an animal or daily quest using a generic CreateView.
    """
    model = Constraints
    template_name = 'fpiweb/constraint_edit.html'
    context_object_name = 'constraint_edit_context'

    formClass = ConstraintsForm

    # TODO Why are fields required here in the create - 1/18/17
    fields = ['constraint_name', 'constraint_descr', 'constraint_type',
              'constraint_min', 'constraint_max', 'constraint_list', ]

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(ConstraintCreateView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:constraint_new')
        return context

    def get_success_url(self):
        """
        Run once form is successfully validated.

        :return:
        """
        results = reverse('fpiweb:constraints_view')
        return results


class ConstraintUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an animal or daily quest using a generic UpdateView.
    """

    model = Constraints
    template_name = 'fpiweb/constraint_edit.html'
    context_object_name = 'constraint_edit_context'

    form_class = ConstraintsForm

    # TODO Why are fields forbidden here in the update - 1/18/17
    # fields = ['category', 'constraints_order', 'constraints_name',
    # 'date_started', ]

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(ConstraintUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:constraint_update',
                                    kwargs={'pk': self.get_object().id})
        return context

    def get_success_url(self):
        """
        Set the next URL to use once the edit is successful.
        :return:
        """

        results = reverse('fpiweb:constraints_view')
        return results


class ConstraintDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete an animal or daily quest using a generic DeleteView.
    """
    model = Constraints
    template_name = 'fpiweb/constraint_delete.html'
    context_object_name = 'constraint_delete_context'

    def get_success_url(self):
        """
        Set the next URL to use once the delete is successful.
        :return:
        """

        results = reverse('fpiweb:constraints_view')
        return results

# EOF
