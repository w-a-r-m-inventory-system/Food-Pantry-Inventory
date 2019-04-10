"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from typing import Union, Optional

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView, FormView

from fpiweb.forms import LoginForm, ConstraintsForm
from fpiweb.models import Constraints

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


# def index(request):
#     """
#     Build index.html web page.
#
#     :param request:
#     :return:
#     """
#
#     response = HttpResponse("Hello world from Food Pantry Inventory.")
#     return response


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


class ConstraintsListView(ListView):
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


# class ConstraintDetailView(DetailView):
#     """
#     Show details of a constraint using a generic DetailView.
#     """
#     model = Constraints
#     template_name = 'fpiweb/constraint_detail.html'
#     context_object_name = 'constraint_detail_context'
#     constraint = 'id'
#
#     def get_context_data(self, **kwargs):
#         """
#         Add additional content to the context.
#
#         :param kwargs:
#         :return: context
#         """
#         context = super(ConstraintDetailView, self).get_context_data()
#
#         # provide additional information
#         # ConstraintID = context['id']
#         constraint = context['object']
#
#         # add puzzles
#         constraint_info = Constraints.objects.filter(
#             constraint_id__exact=Constraints.id
#         )
#
#         # add stuff back to context
#         context['constraint'] = constraint
#         context['constraint_info'] = constraint_info
#
#         return context


def validate_constraint_data(con_name: str, con_descr: str,
                             con_type: Constraints.CONSTRAINT_TYPE_CHOICES,
                             con_min: Union[str, int, None],
                             con_max: Union[str, int, None],
                             con_list: Optional[list]) -> tuple:
    """
    Validate the constraint data provided in a web page.

    :param con_name: constraint name
    :param con_descr: constraint description
    :param con_type: constraint type
    :param con_min: constraint minimum
    :param con_max: constraint maximum
    :param con_list: constraint list
    :return: Two part tuple.  First part: True if valid or False if not,
        second part: None if valid, error message(s) if not (as a string)
    """

    # assume valid until proven otherwise.
    valid = True
    msg = ''

    # validation logic
    if not con_name or (len(con_name) < 1):
        msg += "A constraint name must be specified; "
        valid = False

    if not con_descr or (len(con_descr) < 1):
        msg += "A constraint name must be specified; "
        valid = False

    if con_type == Constraints.INT_LIST:
        if con_min or con_max:
            msg += 'Do not specify a minimum or maximum with a list'
            valid = False  # validate that con_list is a list and that it
            # contains all integers
    elif con_type == Constraints.CHAR_LIST:
        if con_min or con_max:
            msg += 'Do not specify a minimum or maximum with a list'
            valid = False  # validate that con_list is a list and and has at
            # least one value
    elif con_type == Constraints.INT_RANGE:
        if con_list:
            msg += 'Do not specify a list with min/max type; '
            valid = False  # validate that min and max contain integers
    elif con_type == Constraints.CHAR_RANGE:
        if con_list:
            msg += 'Do not specify a list with min/max type; '
            valid = False  # validate that min and max contain characters
    else:
        msg += 'A valid constraint tipe must be chosen; '
        valid = False

    # report results
    if valid:
        response = (True, None)
    else:
        response = (False, msg[-2])

    return response


class ConstraintCreateView(CreateView):
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

    def form_valid(self, form):
        """
        Validate the form data before pushing to the database.

        :param form:
        :return:
        """
        cname = form.cleaned_data.get('constraint_name')
        cdescr = form.cleaned_data.get('constraint_descr')
        ctype = form.cleaned_data.get('constraint_type')
        cmin = form.cleaned_data.get('constraint_min')
        cmax = form.cleaned_data.get('constraint_max')
        clist = form.cleaned_data.get('constraint_list')

        Validation_response = validate_constraint_data(con_name=cname,
                                                       con_descr=cdescr,
                                                       con_type=ctype,
                                                       con_min=cmin,
                                                       con_max=cmax,
                                                       con_list=clist)

        if Validation_response[0]:
            form_response = super().form_valid(form)
        else:
            form.add_error(None, Validation_response[1])
            form_response = self.form_invalid(form)

        return form_response

    def get_success_url(self):
        """
        Run once form is successfully validated.

        :return:
        """
        results = reverse('fpiweb:constraints_view')
        return results


class ConstraintUpdateView(UpdateView):
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

    def form_valid(self, form):
        """
        Validate the form data before pushing to the database.

        :param form:
        :return:
        """
        cname = form.cleaned_data.get('constraint_name')
        cdescr = form.cleaned_data.get('constraint_descr')
        ctype = form.cleaned_data.get('constraint_type')
        cmin = form.cleaned_data.get('constraint_min')
        cmax = form.cleaned_data.get('constraint_max')
        clist = form.cleaned_data.get('constraint_list')

        Validation_response = validate_constraint_data(con_name=cname,
                                                       con_descr=cdescr,
                                                       con_type=ctype,
                                                       con_min=cmin,
                                                       con_max=cmax,
                                                       con_list=clist)

        if Validation_response[0]:
            form_response = super().form_valid(form)
        else:
            form.add_error(None, Validation_response[1])
            form_response = self.form_invalid(form)

        return form_response

    def get_success_url(self):
        """
        Set the next URL to use once the edit is successful.
        :return:
        """

        results = reverse('fpiweb:constraints_view')
        return results


class ConstraintDeleteView(DeleteView):
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
