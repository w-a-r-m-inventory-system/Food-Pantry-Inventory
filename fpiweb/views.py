"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from logging import getLogger, debug

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView, FormView

from fpiweb.models import Box, BoxNumber, Constraints
from fpiweb.forms import \
    ConstraintsForm, \
    FillBoxForm, \
    LoginForm, \
    NewBoxForm

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


logger = getLogger('fpiweb')


class IndexView(TemplateView):
    """
    Default web page (/index)
    """
    template_name = 'fpiweb/index.html'


def error_page(
        request,
        message=None,
        message_list=tuple(),
        status=400):

    return render(
        request,
        'fpiweb/error.html',
        {
            'message': message,
            'message_list': message_list,
        },
        status=status
    )


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

    def get_context_data(self, **kwargs):

        logout(self.request)
        nothing = dict()
        return nothing


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
    context_object_name = 'constraint_edit_context/'

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


class BoxNewView(LoginRequiredMixin, View):
    # model = Box
    template_name = 'fpiweb/box_new.html'
    # context_object_name = 'box'
    # form_class = NewBoxForm

    # def get_success_url(self):
    #     return reverse(
    #         'fpiweb:box_details',
    #         args=(self.object.pk,)
    #     )

    def get(self, request, *args, **kwargs):
        box_number = kwargs.get('box_number')
        if not box_number:
            return error_page(request, 'missing box_number')

        if not BoxNumber.validate(box_number):
            return error_page(
                request,
                "Invalid box_number '{}'".format(box_number),
            )

        new_box_form = NewBoxForm(initial={'box_number': box_number})
        return render(
            request,
            self.template_name,
            {
                'form': new_box_form,
            }
        )

    def post(self, request, *args, **kwargs):
        box_number = kwargs.get('box_number')
        if not box_number:
            return error_page(request, 'missing box_number')

        if not BoxNumber.validate(box_number):
            return error_page(
                request,
                "Invalid box_number '{}'".format(box_number),
            )

        new_box_form = NewBoxForm(
            request.POST,
            initial={'box_number': box_number},
        )

        if not new_box_form.is_valid():
            return render(
                request,
                self.template_name,
                {
                    'form': new_box_form,
                },
            )

        box = new_box_form.save()
        return redirect(reverse('fpiweb:box_details', args=(box.pk,)))


class BoxEditView(LoginRequiredMixin, UpdateView):
    model = Box
    template_name = 'fpiweb/box_edit.html'
    context_object_name = 'box'
    form_class = NewBoxForm
    success_url = reverse_lazy('fpiweb:index')


class BoxDetailsView(LoginRequiredMixin, DetailView):

    model = Box
    template_name = 'fpiweb/box_detail.html'
    context_object_name = 'box'

    def get_context_data(self, **kwargs):
        debug(f"kwargs are {kwargs}")
        context = super().get_context_data(**kwargs)
        return context


class BoxEmptyMoveView(LoginRequiredMixin, TemplateView):
    template_name = 'fpiweb/box_empty_move.html'

    def get_context_data(self, **kwargs):
        return {}


class BoxMoveView(LoginRequiredMixin, TemplateView):

    template_name = 'fpiweb/box_move.html'

    def get_context_data(self, **kwargs):
        return {}


class BoxEmptyView(LoginRequiredMixin, View):
    pass


class BoxFillView(LoginRequiredMixin, UpdateView):
    model = Box
    template_name = 'fpiweb/box_fill.html'
    context_object_name = 'box'
    form_class = FillBoxForm

    def get_success_url(self):
        return reverse(
            'fpiweb:box_details',
            args=(self.object.pk,)
        )


class BoxScannedView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        box_number = kwargs.get('number')
        if pk is None:
            return error_page(request, "missing kwargs['number']")
        box_number = BoxNumber.format_box_number(box_number)

        try:
            box = Box.objects.get(box_number=box_number)
        except Box.DoesNotExist:
            return redirect('fpiweb:box_new', box_number=box_number)

        if not box.product:
            return redirect('fpiweb:box_fill', pk=box.pk)

        return redirect('fpiweb:box_details', pk=box.pk)


class TestScanView(LoginRequiredMixin, TemplateView):

    template_name = 'fpiweb/test_scan.html'

    @staticmethod
    def get_box_scanned_url(box_number):
        if box_number.lower().startswith('box'):
            box_number = box_number[3:]
        return reverse('fpiweb:box_scanned', args=(box_number,))

    @staticmethod
    def get_box_url_by_filters(**filters):
        box_number = Box.objects \
            .filter(**filters) \
            .values_list('box_number', flat=True) \
            .first()
        if box_number is None:
            return ""
        return TestScanView.get_box_scanned_url(box_number)

    def get_context_data(self, **kwargs):

        full_box_url = self.get_box_url_by_filters(product__isnull=False)
        empty_box_url = self.get_box_url_by_filters(product__isnull=True)

        new_box_url = self.get_box_scanned_url(
            BoxNumber.get_next_box_number()
        )

        empty_box = Box.objects.filter(product__isnull=True).first()
        full_box = Box.objects.filter(product__isnull=False).first()

        return {
            'full_box_url': full_box_url,
            'empty_box_url': empty_box_url,
            'new_box_url': new_box_url,
            'empty_box': empty_box,
            'full_box': full_box,
            'next_box_number': BoxNumber.get_next_box_number()
        }


# EOF
