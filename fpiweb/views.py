"""
views.py - establish the views (pages) for the F. P. I. web application.
"""

from collections import OrderedDict
from csv import writer as csv_writer
from enum import Enum
from http import HTTPStatus
from io import BytesIO
from json import loads
from logging import getLogger, debug, info
from string import digits
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import \
    LoginRequiredMixin, \
    PermissionRequiredMixin
from django.core.serializers import serialize
from django.db import transaction
from django.db.models import Max
from django.db.models.functions import Substr
from django.forms import formset_factory
from django.http import \
    FileResponse, \
    HttpResponse, \
    JsonResponse, \
    StreamingHttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import \
    CreateView, \
    DeleteView, \
    DetailView, \
    FormView, \
    ListView, \
    TemplateView, \
    UpdateView

from sqlalchemy.engine.url import URL

from fpiweb.constants import \
    ProjectError, \
    InvalidValueError
from fpiweb.models import \
    Activity, \
    Box, \
    BoxNumber, \
    Constraints, \
    LocRow, \
    LocBin, \
    LocTier, \
    Pallet, \
    Product, \
    Profile, \
    Location, \
    PalletBox
from fpiweb.code_reader import \
    CodeReaderError, \
    read_box_number
from fpiweb.forms import \
    BoxItemForm, \
    BoxTypeForm, \
    ConfirmMergeForm, \
    ConstraintsForm, \
    BuildPalletForm, \
    EmptyBoxNumberForm, \
    ExistingBoxTypeForm, \
    ExistingLocationForm, \
    ExistingLocationWithBoxesForm, \
    ExistingProductForm, \
    ExtantBoxNumberForm, \
    ExpYearForm, \
    FilledBoxNumberForm, \
    HiddenPalletForm, \
    LocRowForm, \
    LocBinForm, \
    LocTierForm, \
    LoginForm, \
    MoveToLocationForm, \
    NewBoxForm, \
    NewBoxNumberForm, \
    PalletNameForm, \
    PalletSelectForm, \
    PrintLabelsForm, \
    ProductForm, \
    ExpMoStartForm, \
    ExpMoEndForm, \
    validation_exp_months_bool
from fpiweb.qr_code_utilities import QRCodePrinter
from fpiweb.support.BoxManagement import BoxManagementClass

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

logger = getLogger('fpiweb')


def error_page(
        request,
        message=None,
        message_list=tuple(),
        status=HTTPStatus.BAD_REQUEST):

    return render(
        request,
        'fpiweb/error.html',
        {
            'message': message,
            'message_list': message_list,
        },
        status=status
    )


def get_user_and_profile(request):
    user = request.user
    profile = user.profile or Profile.objects.create(user=user)
    return user, profile


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Default web page (/index)
    """
    template_name = 'fpiweb/index.html'

    def get_context_data(self, **kwargs):
        """
        Add some security info so appropriate links can be hidden.

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        profile=Profile.objects.get(user=current_user)
        context={
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'title': profile.title,
            'email': current_user.email
        }
        return context


class AboutView(TemplateView):
    """
    The About View for this application.
    """

    template_name = 'fpiweb/about.html'
    context_object_name = 'about_context'

    def get_context_data(self, **kwargs):
        """
        Add Site Information to About page.

        :param kwargs:
        :return:
        """

        # get this information from the database later
        context = super().get_context_data(**kwargs)
        site_name = 'WARM (Westerville Area Resource Ministries)'
        site_address = '150 Heatherdown Dr.'
        site_csz = 'Westerville Ohio 43081'
        site_phone = '614-899-0196'
        site_url = 'http://www.warmwesterville.org'
        context['site_name'] = site_name
        context['site_address'] = site_address
        context['site_csz'] = site_csz
        context['site_phone'] = site_phone
        context['site_url'] = site_url
        return context


class LoginView(FormView):
    template_name = 'fpiweb/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('fpiweb:index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(
            request=self.request,
            username=username,
            password=password
        )

        if user is None:
            form.add_error(None, "Invalid username and/or password")
            return self.form_invalid(form)

        login(self.request, user)
        profile = Profile.objects.get_or_create(
            user_id=user.id,
            defaults={'title': 'User'},
        )

        return super().form_valid(form)


class LogoutView(TemplateView):
    template_name = 'fpiweb/logout.html'

    def get_context_data(self, **kwargs):
        logout(self.request)
        nothing = dict()
        return nothing


class MaintenanceView(PermissionRequiredMixin, TemplateView):
    """
    Default web page (/index)
    """

    permission_required = (
        'fpiweb.view_system_maintenance',
    )

    template_name = 'fpiweb/maintenance.html'


class LocRowListView(PermissionRequiredMixin, ListView):
    """
    List of existing rows using a generic ListView.
    """

    permission_required = (
        'fpiweb.view_locrow',
    )

    model = LocRow
    template_name = 'fpiweb/loc_row_list.html'
    context_object_name = 'loc_row_list_content'


class LocRowCreateView(PermissionRequiredMixin, CreateView):
    """
    Create a row using a generic CreateView.
    """

    permission_required = (
        'fpiweb.add_locrow',
    )

    model = LocRow
    template_name = 'fpiweb/loc_row_edit.html'
    context_object_name = 'loc_row'
    success_url = reverse_lazy('fpiweb:loc_row_view')

    formClass = LocRowForm

    fields = ['loc_row', 'loc_row_descr', ]


class LocRowUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Update a row using a generic UpdateView.
    """

    permission_required = (
        'fpiweb.change_locrow',
    )

    model = LocRow
    template_name = 'fpiweb/loc_row_edit.html'
    context_object_name = 'loc_row'
    form_class = LocRowForm
    success_url = reverse_lazy('fpiweb:loc_row_view')


class LocRowDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Delete a row using a generic DeleteView.
    """

    permission_required = (
        'fpiweb.delete_locrow',
    )

    model = LocRow
    template_name = 'fpiweb/loc_row_delete.html'
    context_object_name = 'loc_row'
    success_url = reverse_lazy('fpiweb:loc_row_view')

    form_class = LocRowForm

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(LocRowDeleteView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:loc_row_delete',
                                    kwargs={'pk': self.get_object().id})
        return context


class LocBinListView(PermissionRequiredMixin, ListView):
    """
    List of existing bins using a generic ListView.
    """
    permission_required = (
        'fpiweb.view_locbin',
    )

    model = LocBin
    template_name = 'fpiweb/loc_bin_list.html'
    context_object_name = 'loc_bin_list_content'


class LocBinCreateView(PermissionRequiredMixin, CreateView):
    """
    Create a bin using a generic CreateView.
    """

    permission_required = (
        'fpiweb.add_locbin',
    )

    model = LocBin
    template_name = 'fpiweb/loc_bin_edit.html'
    context_object_name = 'loc_bin'
    success_url = reverse_lazy('fpiweb:loc_bin_view')

    formClass = LocBinForm

    fields = ['loc_bin', 'loc_bin_descr', ]


class LocBinUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Update a bin using a generic UpdateView.
    """

    permission_required = (
        'fpiweb.change_locbin',
    )

    model = LocBin
    template_name = 'fpiweb/loc_bin_edit.html'
    context_object_name = 'loc_bin'
    success_url = reverse_lazy('fpiweb:loc_bin_view')

    form_class = LocBinForm

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(LocBinUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:loc_bin_update',
                                    kwargs={'pk': self.get_object().id})
        return context


class LocBinDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Delete a bin using a generic DeleteView.
    """

    permission_required = (
        'fpiweb.delete_locbin',
    )

    model = LocBin
    template_name = 'fpiweb/loc_bin_delete.html'
    context_object_name = 'loc_bin'
    success_url = reverse_lazy('fpiweb:loc_bin_view')

    form_class = LocBinForm

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(LocBinDeleteView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:loc_bin_delete',
                                    kwargs={'pk': self.get_object().id})
        return context


class LocTierListView(PermissionRequiredMixin, ListView):
    """
    List of existing tiers using a generic ListView.
    """

    permission_required = (
        'fpiweb.view_loctier',
    )

    model = LocTier
    template_name = 'fpiweb/loc_tier_list.html'
    context_object_name = 'loc_tier_list_content'


class LocTierCreateView(PermissionRequiredMixin, CreateView):
    """
    Create a tier using a generic CreateView.
    """

    permission_required = (
        'fpiweb.add_loctier',
    )

    model = LocTier
    template_name = 'fpiweb/loc_tier_edit.html'
    context_object_name = 'loc_tier'
    success_url = reverse_lazy('fpiweb:loc_tier_view')

    formClass = LocTierForm

    fields = ['loc_tier', 'loc_tier_descr', ]


class LocTierUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Update a tier using a generic UpdateView.
    """

    permission_required = (
        'fpiweb.change_loctier',
    )

    model = LocTier
    template_name = 'fpiweb/loc_tier_edit.html'
    context_object_name = 'loc_tier'
    success_url = reverse_lazy('fpiweb:loc_tier_view')

    form_class = LocTierForm

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(LocTierUpdateView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:loc_tier_update',
                                    kwargs={'pk': self.get_object().id})
        return context


class LocTierDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Delete a tier using a generic DeleteView.
    """

    permission_required = (
        'fpiweb.delete_loctier',
    )

    model = LocTier
    template_name = 'fpiweb/loc_tier_delete.html'
    context_object_name = 'loc_tier'
    success_url = reverse_lazy('fpiweb:loc_tier_view')

    form_class = LocTierForm

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(LocTierDeleteView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:loc_tier_delete',
                                    kwargs={'pk': self.get_object().id})
        return context


class ConstraintsListView(PermissionRequiredMixin, ListView):
    """
    List of existing constraints.
    """

    permission_required = (
        'fpiweb.view_constraints',
    )

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
        info(
            f'Constraint extra info: INT_RANGE: {INT_RANGE}, '
            f'CHAR__RANGE: '
            f'{CHAR_RANGE}, range_list: {range_list}'
        )

        return context


class ConstraintCreateView(PermissionRequiredMixin, CreateView):
    """
    Create a constraint using a generic CreateView.
    """

    permission_required = (
        'fpiweb.add_constraints',
    )

    model = Constraints
    template_name = 'fpiweb/constraint_edit.html'
    context_object_name = 'constraints'
    success_url = reverse_lazy('fpiweb:constraints_view')

    formClass = ConstraintsForm

    fields = ['constraint_name', 'constraint_descr', 'constraint_type',
              'constraint_min', 'constraint_max', 'constraint_list', ]


class ConstraintUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Update a constraint using a generic UpdateView.
    """

    permission_required = (
        'fpiweb.change_constraints',
    )

    model = Constraints
    template_name = 'fpiweb/constraint_edit.html'
    context_object_name = 'constraints'

    form_class = ConstraintsForm

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


class ConstraintDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Delete a constraint using a generic DeleteView.
    """

    permission_required = (
        'fpiweb.delete_constraints',
    )

    model = Constraints
    template_name = 'fpiweb/constraint_delete.html'
    context_object_name = 'constraints'
    success_url = reverse_lazy('fpiweb:constraints_view')

    form_class = ConstraintsForm

    def get_context_data(self, **kwargs):
        """
        Modify the context before rendering the template.

        :param kwargs:
        :return:
        """

        context = super(ConstraintDeleteView, self).get_context_data(**kwargs)
        context['action'] = reverse('fpiweb:constraint_delete',
                                    kwargs={'pk': self.get_object().id})
        return context


class BoxNewView(PermissionRequiredMixin, View):
    # model = Box

    permission_required = (
        'fpiweb.dummy_profile',
    )

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


class BoxEditView(PermissionRequiredMixin, UpdateView):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    model = Box
    template_name = 'fpiweb/box_edit.html'
    context_object_name = 'box'
    form_class = NewBoxForm
    success_url = reverse_lazy('fpiweb:index')


class BoxDetailsView(PermissionRequiredMixin, DetailView):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    model = Box
    template_name = 'fpiweb/box_detail.html'
    context_object_name = 'box'

    def get_context_data(self, **kwargs):
        logger.debug(f"kwargs are {kwargs}")
        context = super().get_context_data(**kwargs)
        return context


class BoxEmptyMoveView(PermissionRequiredMixin, TemplateView):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    template_name = 'fpiweb/box_empty_move.html'

    def get_context_data(self, **kwargs):
        return {}


class BoxMoveView(PermissionRequiredMixin, TemplateView):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    template_name = 'fpiweb/box_empty_move.html'

    def get_context_data(self, **kwargs):
        return {}


class BoxEmptyView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.dummy_profile',
    )


class BoxScannedView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    def get(self, request, **kwargs):
        box_number = kwargs.get('number')
        if box_number is None:
            return error_page(request, "missing kwargs['number']")
        box_number = BoxNumber.format_box_number(box_number)

        try:
            box = Box.objects.get(box_number=box_number)
        except Box.DoesNotExist:
            return redirect('fpiweb:box_new', box_number=box_number)

        return redirect('fpiweb:build_pallet', args=(box.pk,))


class TestScanView(PermissionRequiredMixin, TemplateView):

    permission_required = (
        'fpiweb.dummy_profile',
    )

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

        # schema http or https
        schema = 'http'
        if settings.DEBUG is False and hasattr(self.request, 'schema'):
            schema = self.request.schema

        protocol_and_host = "{}://{}".format(
            schema,
            self.request.META.get('HTTP_HOST', '')
        )

        full_box_url = protocol_and_host + full_box_url
        empty_box_url = protocol_and_host + empty_box_url
        new_box_url = protocol_and_host + new_box_url

        empty_box = Box.objects.filter(product__isnull=True).first()
        full_box = Box.objects.filter(product__isnull=False).first()

        return {
            'full_box_url': full_box_url,
            'empty_box_url': empty_box_url,
            'new_box_url': new_box_url,
            'empty_box': empty_box,
            'full_box': full_box,
            'next_box_number': BoxNumber.get_next_box_number(),
        }


class BuildPalletError(RuntimeError):
    pass


class BuildPalletView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.build_pallet',
    )

    form_template = 'fpiweb/build_pallet.html'
    confirmation_template = 'fpiweb/build_pallet_confirmation.html'

    build_pallet_form_prefix = 'build_pallet'
    formset_prefix = 'box_forms'
    hidden_pallet_form_prefix = 'pallet'

    page_title = 'Build Pallet'

    BoxFormFactory = formset_factory(
        BoxItemForm,
        extra=0,
    )

    PALLET_SELECT_FORM_NAME = 'pallet_select_form'
    PALLET_NAME_FORM_NAME = 'pallet_name_form'

    def show_forms_response(
            self,
            request,
            build_pallet_form,
            box_forms,
            pallet_form,
            status=HTTPStatus.BAD_REQUEST):
        """
        Display page with BuildPalletForm and BoxItemForms
        :param request:
        :param build_pallet_form:
        :param box_forms:
        :param pallet_form:
        :param status:
        :return:
        """

        return render(
            request,
            self.form_template,
            {
                'form': build_pallet_form,
                'box_forms': box_forms,
                'pallet_form': pallet_form,
            },
            status=status,
        )

    @staticmethod
    def show_pallet_management_page(
            request,
            pallet_select_form=None,
            pallet_name_form=None,
            status_code=HTTPStatus.OK):

        return PalletManagementView.show_page(
            request,
            page_title=BuildPalletView.page_title,
            prompt="Select an existing pallet or create a new one to continue",
            show_delete=False,
            pallet_select_form=pallet_select_form,
            pallet_name_form=pallet_name_form,
            status_code=status_code,
        )

    def get(self, request):
        # Show page to select/add new pallet.  This page will POST back to this
        # view
        return self.show_pallet_management_page(request)

    def post(self, request):
        # BuildPalletView.post

        logger.debug(f"POST data is {request.POST}")

        # The forms in pallet_management.html have a form_name input to help
        # us sort out which form is being submitted.
        form_name = request.POST.get('form_name')

        if form_name is None:
            # Processing contents of build_pallet.html
            return self.process_build_pallet_forms(request)

        if form_name not in [
            self.PALLET_SELECT_FORM_NAME,
            self.PALLET_NAME_FORM_NAME
        ]:
            message = f"Unexpected form name {repr(form_name)}"
            logger.error(message)
            return error_page(
                request,
                message=message,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        pallet = None
        if form_name == self.PALLET_SELECT_FORM_NAME:
            pallet_select_form = PalletSelectForm(request.POST)
            if not pallet_select_form.is_valid():
                return self.show_pallet_management_page(
                    request,
                    pallet_select_form=pallet_select_form,
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            pallet = pallet_select_form.cleaned_data.get('pallet')
            pallet.pallet_status = Pallet.FILL

        if form_name == self.PALLET_NAME_FORM_NAME:
            pallet_name_form = PalletNameForm(request.POST)
            if not pallet_name_form.is_valid():
                return self.show_pallet_management_page(
                    request,
                    pallet_name_form=pallet_name_form,
                    status_code=HTTPStatus.BAD_REQUEST,
                )
            pallet_name_form.instance.pallet_status = Pallet.FILL
            pallet = pallet_name_form.save()

        if not pallet:
            message = f"pallet not set"
            logger.error(message)
            return error_page(
                request,
                message=message,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        # Load boxes (PalletBox records) for pallet
        pallet_boxes = pallet.boxes.all()

        initial_data = []
        for pallet_box in pallet_boxes:
            form_data = {
                'box_number': pallet_box.box_number,
                'product': pallet_box.product,
                'exp_year': pallet_box.exp_year,
                'exp_month_start': pallet_box.exp_month_start,
                'exp_month_end': pallet_box.exp_month_end,
            }
            print("adding {} to initial_data".format(form_data))
            initial_data.append(form_data)

        build_pallet_form = BuildPalletForm(
            prefix=self.build_pallet_form_prefix,
            instance=pallet.location,
        )

        box_forms = self.BoxFormFactory(
            initial=initial_data,
            prefix=self.formset_prefix,
        )

        pallet_form = HiddenPalletForm(
            prefix=self.hidden_pallet_form_prefix,
            initial={
                'pallet': pallet,
            },
        )

        return self.show_forms_response(
            request,
            build_pallet_form,
            box_forms,
            pallet_form,
            status=HTTPStatus.OK,
        )

    @staticmethod
    def prepare_pallet_and_pallet_boxes(
        pallet_form,
        build_pallet_form,
        box_forms,
    ):
        location = build_pallet_form.instance

        pallet = pallet_form.cleaned_data.get('pallet')
        pallet.location = location
        pallet.pallet_status = Pallet.FILL
        pallet.save()

        # Update box records and
        boxes_by_box_number = OrderedDict()
        duplicate_box_numbers = set()
        for i, box_form in enumerate(box_forms):
            cleaned_data = box_form.cleaned_data
            if not cleaned_data:
                continue

            box_number = cleaned_data.get('box_number')

            # Is this a duplicate box_id?
            if box_number in boxes_by_box_number:
                duplicate_box_numbers.add(box_number)
                continue

            # Is box_number present in database?
            try:
                pallet_box = PalletBox.objects.get(
                    pallet=pallet,
                    box_number=box_number
                )
                logger.debug(f"found existing box {box_number}")
            except PalletBox.DoesNotExist:
                pallet_box = PalletBox(
                    box_number=box_number,
                )
                logger.debug(f"Created new box {box_number}")

            pallet_box.pallet = pallet
            pallet_box.product = cleaned_data.get('product')
            pallet_box.exp_year = cleaned_data.get('exp_year')
            pallet_box.exp_month_start = cleaned_data.get('exp_month_start', 0)
            pallet_box.exp_month_end = cleaned_data.get('exp_month_end', 0)

            # Does the pallet_box have a box?
            if not pallet_box.box:
                box, created = Box.objects.get_or_create(
                    box_number=box_number,
                    box_type=Box.box_type_default(),
                )
                pallet_box.box = box

            pallet_box.save()

            boxes_by_box_number[box_number] = pallet_box

            # When the box was scanned it would have been emptied if it was
            # filled.  This catches whether anything has changed.
            if pallet_box.box.is_filled():
                box_management = BoxManagementClass()
                box_management.box_consume(pallet_box.box)

        if duplicate_box_numbers:
            duplicate_box_numbers = [str(k) for k in duplicate_box_numbers]
            message = f"Duplicate box numbers: {', '.join(duplicate_box_numbers)}"
            logger.debug(message)
            build_pallet_form.add_error(None, message)
            raise BuildPalletError(message)

        return pallet, location, boxes_by_box_number

    def process_build_pallet_forms(self, request):

        build_pallet_form = BuildPalletForm(
            request.POST,
            prefix=self.build_pallet_form_prefix
        )
        box_forms = self.BoxFormFactory(
            request.POST,
            prefix=self.formset_prefix,
        )
        pallet_form = HiddenPalletForm(
            request.POST,
            prefix=self.hidden_pallet_form_prefix,
        )

        build_pallet_form_valid = build_pallet_form.is_valid()
        if not build_pallet_form_valid:
            logger.debug("BuildPalletForm not valid")

        box_forms_valid = box_forms.is_valid()
        if not box_forms_valid:
            logger.debug("BoxForms not valid")

        pallet_form_valid = pallet_form.is_valid()
        if not pallet_form_valid:
            logger.debug("HiddenPalletForm not valid")

        if not all([
            build_pallet_form_valid,
            box_forms_valid,
            pallet_form_valid
        ]):
            return self.show_forms_response(
                request,
                build_pallet_form,
                box_forms,
                pallet_form,
            )

        try:
            pallet, location, boxes_by_box_number = \
                self.prepare_pallet_and_pallet_boxes(
                    pallet_form,
                    build_pallet_form,
                    box_forms,
                )
        except BuildPalletError:
            return self.show_forms_response(
                request,
                build_pallet_form,
                box_forms,
                pallet_form,
            )

        box_management = BoxManagementClass()
        box_management.pallet_finish(pallet)

        return render(
            request,
            self.confirmation_template,
            {
                'location': location,
                'boxes': boxes_by_box_number.values(),
            },
        )


class ScannerViewError(RuntimeError):
    pass


class ScannerView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    @staticmethod
    def response(
            success,
            data=None,
            errors=None, status=HTTPStatus.OK,
    ):
        return JsonResponse(
            {
                'success': success,
                'data': data if data else {},
                'errors': errors if errors else [],
            },
            status=status
        )

    @staticmethod
    def error_response(errors, status=HTTPStatus.BAD_REQUEST):
        return ScannerView.response(
            False,
            errors,
            status=status
        )

    @staticmethod
    def get_keyed_in_box_number(box_number):
        """
        :param box_number: the box number (a string), may be None
        :return:
        """
        box_number = box_number or ''
        if not box_number:
            return None

        # strip out everything, but digits
        box_number = "".join(c for c in box_number if c in digits)
        if not box_number:
            return None

        try:
            box_number = int(box_number)
        except ValueError:
            return None

        return BoxNumber.format_box_number(box_number)

    @staticmethod
    def get_box(scan_data=None, box_number=None):
        if not scan_data and not box_number:
            raise ScannerViewError('missing scan_data and box_number')

        if not box_number:
            try:
                box_number = read_box_number(scan_data)
            except CodeReaderError as cre:
                raise ScannerViewError(str(cre))

        default_box_type = Box.box_type_default()

        box, created = Box.objects.get_or_create(
            box_number=box_number,
            defaults={
                'box_type': default_box_type,
                'quantity': default_box_type.box_type_qty,
            }
        )
        if created:
            logger.info(f"Box with box number {box_number} created.")
        else:
            logger.info(f"Found box with box number {box_number}.")
        return box, created

    @staticmethod
    def get_box_data(scan_data=None, box_number=None):

        box, created = ScannerView.get_box(
            scan_data=scan_data,
            box_number=box_number
        )

        # serialize works on an iterable of objects and returns a string
        # loads returns a list of dicts
        box_dicts = loads(serialize("json", [box]))

        data = {
            'box': box_dicts[0],
            'box_meta': {
                'is_new': created,
            }
        }
        return data

    def post(self, request, *args, **kwargs):

        scan_data = request.POST.get('scanData')
        box_number = self.get_keyed_in_box_number(
            request.POST.get('boxNumber'),
        )

        try:
            box_data = self.get_box_data(scan_data, box_number)
        except ScannerViewError as sve:
            error_message = str(sve)
            logger.error(error_message)
            return self.error_response([error_message])

        return self.response(
            True,
            data=box_data,
            status=HTTPStatus.OK,
        )


class PrintLabelsView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.print_labels_box',
    )

    template_name = 'fpiweb/print_labels.html'

    @staticmethod
    def get_base_url(meta):
        protocol = meta.get('SERVER_PROTOCOL', 'HTTP/1.1')
        protocol = protocol.split('/')[0].lower()

        host = meta.get('HTTP_HOST')
        return f"{protocol}://{host}/"

    def get(self, request, *args, **kwargs):
        max_box_number = Box.objects.aggregate(Max('box_number'))
        print("max_box_number", max_box_number)

        return render(
            request,
            self.template_name,
            {'form': PrintLabelsForm()}
        )

    def post(self, request, *args, **kwargs):
        base_url = self.get_base_url(request.META)

        form = PrintLabelsForm(request.POST)
        if not form.is_valid():
            print("form invalid")
            return render(
                request,
                self.template_name,
                {'form': form},
            )
        print("form valid")

        buffer = BytesIO()

        QRCodePrinter(url_prefix='').print(
            starting_number=form.cleaned_data.get('starting_number'),
            count=form.cleaned_data.get('number_to_print'),
            buffer=buffer,
        )

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='labels.pdf')


class BoxItemFormView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.add_box',
    )

    template_name = 'fpiweb/box_form.html'

    @staticmethod
    def get_form(pallet_box, prefix=None):
        kwargs = {
            'initial': BoxItemForm.get_initial_from_box(pallet_box)
        }
        if prefix:
            kwargs['prefix'] = prefix
        form = BoxItemForm(**kwargs)
        return form

    def post(self, request):

        scan_data = request.POST.get('scanData')
        box_number = ScannerView.get_keyed_in_box_number(
            request.POST.get('boxNumber'),
        )
        prefix = request.POST.get('prefix')
        pallet_pk = request.POST.get('palletPk')

        try:
            box, created = ScannerView.get_box(scan_data, box_number)
        except ScannerViewError as sve:
            error = str(sve)
            logger.error(error)
            return HttpResponse("Scan failed.", status=HTTPStatus.NOT_FOUND)

        try:
            pallet = Pallet.objects.get(pk=pallet_pk)
        except Pallet.DoesNotExist as dne:
            error = f"Pallet pk={pallet_pk} not found"
            logger.error(error)
            return HttpResponse(error, status=HTTPStatus.NOT_FOUND)

        # If box is filled, empty it before continuing
        if box.is_filled():
            box_management = BoxManagementClass()
            box_management.box_consume(box)

        # Look for PalletBox record
        pallet_box, created = PalletBox.objects.get_or_create(
            box_number=box.box_number,
            box=box,
            pallet=pallet
        )

        return render(
            request,
            self.template_name,
            {
                'box_number': box.box_number,
                'form': self.get_form(
                    pallet_box,
                    prefix),
            },
        )


class ManualMenuView(PermissionRequiredMixin, TemplateView):
    """
    Menu to choose between manual pallet or manual box management
    """

    permission_required = (
        'fpiweb.view_pallet',
    )

    template_name = 'fpiweb/manual_menu.html'

    def get_context_data(self, **kwargs):
        """
        Add User Information to Manual Menu page.

        :param kwargs:
        :return:
        """

        # get information from the database
        context = super(ManualMenuView, self).get_context_data(**kwargs)

        # get the current user and related profile
        current_user = self.request.user
        profile = current_user.profile
        if profile:
            active_pallet = profile.active_pallet
        else:
            active_pallet = None

        # does user have active pallet?  if so get info
        if active_pallet:
            new_target = None
            # pallet_rec = Pallet.objects.select_related().get(
            #     id=profile.active_pallet)
            pallet_id = active_pallet.id
            pallet_target = reverse_lazy(
                'fpiweb:manual_pallet_status', args=[pallet_id]
            )
        else:
            new_target = reverse_lazy('fpiweb:manual_pallet_new')
            pallet_target = None

        # load up  the context for the template
        context['current_user'] = current_user
        context['user_profile'] = profile
        context['active_pallet'] = active_pallet
        context['new_target'] = new_target
        context['pallet_target'] = pallet_target
        return context


class ManualPalletMenuView(PermissionRequiredMixin, TemplateView):
    """
    Menu of choices for manual pallet management.
    """

    permission_required = (
        'fpiweb.view_pallet',
    )

    template_name = 'fpiweb/manual_pallet_menu.html'

    def get_context_data(self, **kwargs):
        """
        Add User Information to Manual Menu page.

        :param kwargs:
        :return:
        """

        # get information from the database
        context = super().get_context_data(**kwargs)

        # get the current user and related profile
        current_user = self.request.user
        profile = current_user.profile
        if profile and profile.active_pallet:
            active_pallet = profile.active_pallet
            pallet_boxes = PalletBox.objects.filter(pallet=active_pallet)
            box_set = list()
            for box in pallet_boxes:
                box_set.append(box)
        else:
            active_pallet = None
            box_set = None

        # does user have active pallet?  if so get info
        if active_pallet:
            new_target = None
            # pallet_rec = Pallet.objects.select_related().get(
            #     id=profile.active_pallet)
            pallet_id = active_pallet.id
            pallet_target = reverse_lazy(
                'fpiweb:manual_pallet_status', args=[pallet_id]
            )
        else:
            new_target = reverse_lazy('fpiweb:manual_pallet_new')
            pallet_target = None

        # load up  the context for the template
        context['current_user'] = current_user
        context['user_profile'] = profile
        context['active_pallet'] = active_pallet
        context['box_set'] = box_set
        context['new_target'] = new_target
        context['pallet_target'] = pallet_target
        return context


class ManualBoxMenuView(PermissionRequiredMixin, TemplateView):
    """
    Menu of choices for manual individual box management.
    """
    permission_required = (
        'fpiweb.view_box',
    )

    template_name = 'fpiweb/manual_ind_box_menu.html'

    def get_context_data(self, **kwargs):
        """
        Add User Information to Manual Menu page.

        :param kwargs:
        :return:
        """

        # get information from the database
        context = super().get_context_data(**kwargs)

        # get the current user and related profile
        current_user = self.request.user
        profile = current_user.profile

        # load up  the context for the template
        context['current_user'] = current_user
        context['user_profile'] = profile
        return context


# class ManualNotification(LoginRequiredMixin, TemplateView):
#     """
#     Ask a question or notify the user of something.
#     """
#     template_name = 'fpiweb/manual_generic_notification.html'
#
#     def get_context_data(self, **kwargs):
#         """
#         Get info from reqest and populate context from it.
#
#         :param kwargs:
#         :return:
#         """
#         context = super(ManualNotification, self.get_context_data(**kwargs))
#         request = context.get_request()
#         title = request.


class MANUAL_NOTICE_TYPE(Enum):
    """
    Manual generic notice type.
    """
    NOTICE:str = 'NOTICE'
    QUESTION:str = 'QUESTION'


def manual_generic_notification(
        request,
        note_type: MANUAL_NOTICE_TYPE,
        title: str = None,
        message_list: tuple = tuple(),
        action_message: str = '',
        yes_url: str = 'fpiweb:about',
        no_url: str = 'fpiweb:about',
        return_url: str = 'fpiweb:about',
        status: int = HTTPStatus.OK,
):
    """
    Provide a generic notification screen for the manual box subsystem.

    :param request: request info from calling view
    :param note_type: type of notice (error or note)
    :param title: title to use for notification
    :param message_list: List of lines to display in notification
    :param action_message: final message or question
    :param yes_url: if question, url for yes action
    :param no_url: if question, url for no action
    :param return_url: if notice, url to go to after notification
    :param status: status code to flag notification if needed
    :return:
    """
    # request simply passed on to render
    # template name set to fpiweb:manual_generic_notification

    # context: build contest for template
    context = dict()
    context['type'] = note_type
    context['title'] = title
    context['message_list'] = message_list
    context['action_message'] = action_message
    context['yes_url'] = yes_url
    context['no_url'] = no_url
    context['return_url'] = return_url

    # content_type: use response status from HTTPStatus
    template_info = render(
        request,
        'fpiweb/manual_generic_notification.html',
        context=context,
        status=status,
    )
    return template_info


class ManualPalletNew(LoginRequiredMixin, TemplateView):
    """
    Establish a new pallet for this user.
    """
    # use CreateView later

    model = Profile
    template_name = 'fpiweb/manual_pallet_add.html'
    context_object_name = 'manual_pallet'

    # success_url = reverse_lazy('fpiweb:manual_pallet_status')

    def get_context_data(self, **kwargs):
        """
        Add Site Information to About page.

        :param kwargs:
        :return:
        """

        # get information from the database
        context = super(ManualPalletNew, self).get_context_data(**kwargs)
        current_user = self.request.user
        user_profile = Profile.objects.select_related().get(
            user_id=current_user.id)

        # check if new pallet or other status
        if user_profile.active_location_id:
            # check status
            ...
        else:
            # find new location
            ...

        # load up  the context for the template
        context['current_user'] = current_user
        context['user_profile'] = user_profile
        return context

    def get_success_url(self, **kwargs) -> URL:
        """

        :param kwargs:
        :return:
        """

        current_user = self.request.user
        user_profile = Profile.objects.select_related().get(id=current_user.id)
        pallet_rec = Pallet.objects.select_related().get(
            user_id_id=current_user.id)
        pallet_id = pallet_rec.id
        target = reverse_lazy('fpiweb:manual_pallet_status', args=[pallet_id])
        return target


class ManualPalletStatus(PermissionRequiredMixin, ListView):
    """
    Establish a new pallet for this user.
    """

    permission_required = (
        'fpiweb.dummy_profile',
    )

    model = Pallet
    template_name = 'fpiweb/manual_pallet_status.html'
    context_object_name = 'manual_pallet_status'
    success_url = reverse_lazy('fpiweb:manual_menu')

    def get_(self, **kwargs):
        """
        Add Site Information to About page.

        :param kwargs:
        :return:
        """

        # get stuff from the request
        context = super().get_context_data(**kwargs)

        # get related stuff from the database
        current_user = self.request.user
        profile_rec = Profile.objects.get(user_id=current_user.id)
        if profile_rec.active_pallet:
            pallet_rec = Pallet.objects.select_related(
                'location',
                'location__loc_row',
                'location__loc_bin',
                'location__loc_tier',
            ).get(id=profile_rec.active_pallet)
            location_rec = pallet_rec.location
            loc_row_rec = location_rec.loc_row
            loc_bin_rec = location_rec.loc_bin
            loc_tier_rec = location_rec.loc_tier
            box_set = PalletBox.objects.filter(
                pallet_id=pallet_rec.id).order_by('box_number')
        else:
            pallet_rec = None
            location_rec = None
            loc_row_rec = None
            loc_bin_rec = None
            loc_tier_rec = None
            box_set = None

        context['user'] = current_user
        context['profile'] = profile_rec
        context['active_pallet'] = pallet_rec
        context['location'] = location_rec
        context['loc_row'] = loc_row_rec
        context['loc_bin'] = loc_bin_rec
        context['loc_tier'] = loc_tier_rec
        context['box_set'] = box_set
        return context


class ManualPalletMoveView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.move_pallet',
    )

    MODE_ENTER_FROM_LOCATION = 'enter from location'
    MODE_ENTER_TO_LOCATION = 'enter to location'
    MODE_CONFIRM_MERGE = 'confirm merge'
    MODE_COMPLETE = 'complete'

    FORM_PREFIX_FROM_LOCATION = 'from'
    FORM_PREFIX_TO_LOCATION = 'to'
    FORM_PREFIX_CONFIRM_MERGE = 'confirm_merge'

    template = 'fpiweb/manual_pallet_move.html'

    def get(self, request):
        return self.build_response(
            request,
            self.MODE_ENTER_FROM_LOCATION,
            from_location_form=ExistingLocationWithBoxesForm(
                prefix=self.FORM_PREFIX_FROM_LOCATION,
            )
        )

    def post(self, request):
        mode = request.POST.get('mode')
        if not mode:
            return self.build_response(
                request,
                self.MODE_ENTER_FROM_LOCATION,
                from_location_form=ExistingLocationWithBoxesForm(
                    prefix=self.FORM_PREFIX_FROM_LOCATION,
                ),
                errors=["Missing mode parameter"],
                status=HTTPStatus.BAD_REQUEST,
            )

        if mode == self.MODE_ENTER_FROM_LOCATION:
            return self.post_from_location_form(request)
        if mode == self.MODE_ENTER_TO_LOCATION:
            return self.post_to_location_form(request)
        if mode == self.MODE_CONFIRM_MERGE:
            return self.post_confirm_merge_form(request)
        return error_page(
            request,
            f"Unrecognized mode {mode} in ManualPalletMoveView"
        )

    def post_from_location_form(self, request):
        from_location_form = ExistingLocationWithBoxesForm(
            request.POST,
            prefix=self.FORM_PREFIX_FROM_LOCATION,
        )
        if not from_location_form.is_valid():
            return self.build_response(
                request,
                self.MODE_ENTER_FROM_LOCATION,
                from_location_form=from_location_form,
                status=HTTPStatus.BAD_REQUEST,
            )

        from_location = from_location_form.cleaned_data.get('location')
        return self.show_to_location_form(
            request,
            from_location,
        )

    def show_to_location_form(self, request, from_location):
        return self.build_response(
            request,
            self.MODE_ENTER_TO_LOCATION,
            to_location_form=MoveToLocationForm(
                prefix=self.FORM_PREFIX_TO_LOCATION,
                initial={
                    'from_location': from_location,
                }
            )
        )

    def post_to_location_form(self, request):
        to_location_form = MoveToLocationForm(
            request.POST,
            prefix=self.FORM_PREFIX_TO_LOCATION,
        )
        if not to_location_form.is_valid():
            return self.build_response(
                request,
                self.MODE_ENTER_TO_LOCATION,
                to_location_form=to_location_form,
                status=HTTPStatus.BAD_REQUEST,
            )

        from_location = to_location_form.cleaned_data['from_location']
        to_location = to_location_form.cleaned_data['location']

        boxes_at_to_location = \
            Box.objects.filter(location=to_location).count()

        if boxes_at_to_location == 0:
            return self.move_boxes(request, from_location, to_location)

        return self.build_response(
            request,
            self.MODE_CONFIRM_MERGE,
            confirm_merge_form=ConfirmMergeForm(
                prefix=self.FORM_PREFIX_CONFIRM_MERGE,
                initial={
                    'from_location': from_location,
                    'to_location': to_location,
                    'boxes_at_to_location': boxes_at_to_location,
                },
            ),
        )

    def post_confirm_merge_form(self, request):
        confirm_merge_form = ConfirmMergeForm(
            request.POST,
            prefix=self.FORM_PREFIX_CONFIRM_MERGE,
        )
        if not confirm_merge_form.is_valid():
            return self.build_response(
                request,
                self.MODE_CONFIRM_MERGE,
                confirm_merge_form=confirm_merge_form,
                status=HTTPStatus.BAD_REQUEST,
            )

        from_location = \
            confirm_merge_form.cleaned_data['from_location']
        to_location = confirm_merge_form.cleaned_data['to_location']
        action = confirm_merge_form.cleaned_data['action']

        if action == ConfirmMergeForm.ACTION_CHANGE_LOCATION:
            # this method sets mode appropriately
            return self.show_to_location_form(
                request,
                from_location,
            )

        return self.move_boxes(request, from_location, to_location)

    @staticmethod
    def get_next_temp_name():
        numbers = Pallet.objects.filter(
            name__startswith='temp'
        ).annotate(
            number=Substr('name', 5),
        ).values_list(
            'number',
            flat=True,
        )

        if not numbers:
            return 'temp1'

        max_number = 0
        for n in numbers:
            try:
                n = int(n)
            except (TypeError, ValueError):
                continue
            if n > max_number:
                max_number = n
        return f"temp{max_number + 1}"

    def move_boxes(self, request, from_location, to_location):

        pallet, box_count = self.get_pallet_and_box_count(
            from_location,
            to_location
        )

        box_manager = BoxManagementClass()
        box_manager.pallet_finish(pallet)

        return self.build_response(
            request,
            self.MODE_COMPLETE,
            boxes_moved=box_count,
            to_location=to_location,
        )

    @staticmethod
    def get_pallet_and_box_count(from_location, to_location):
        # Create temporary Pallet and PalletBox records in order to use
        # pallet_finish
        with transaction.atomic():
            pallet = Pallet.objects.create(
                name=ManualPalletMoveView.get_next_temp_name(),
                location=to_location,
                pallet_status=Pallet.MOVE,
            )

        boxes_to_move = Box.objects.filter(location=from_location)

        pallet_boxes = []
        for box in boxes_to_move:
            pallet_box = PalletBox(
                pallet=pallet,
                box=box,
                product=box.product,
                exp_year=box.exp_year,
                exp_month_start=box.exp_month_start,
                exp_month_end=box.exp_month_end,
            )
            pallet_boxes.append(pallet_box)

        PalletBox.objects.bulk_create(pallet_boxes)
        return pallet, len(pallet_boxes)

    def build_response(
            self,
            request,
            mode,
            from_location_form=None,
            to_location_form=None,
            confirm_merge_form=None,
            boxes_moved=0,
            to_location=None,
            errors=None,
            status=HTTPStatus.OK):

        return render(
            request,
            self.template,
            {
                'mode': mode,
                'view_class': self.__class__,
                'from_location_form': from_location_form,
                'to_location_form': to_location_form,
                'confirm_merge_form': confirm_merge_form,
                'boxes_moved': boxes_moved,
                'to_location': to_location,
                'errors': errors or [],
            },
            status=status,
        )


class ActivityDownloadView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.view_activity',
    )

    date_format = '%m/%d/%Y'

    class Echo:
        """An object that implements just the write method of the file-like
        interface.
        """

        @staticmethod
        def write(value):
            """Write the value by returning it, instead of storing in a buffer."""
            return value

    def write_rows(self):

        yield [
            'Box Number', 'Box Type',
            'Row', 'Bin', 'Tier',
            'Product', 'Product Category',
            'Date Filled', 'Date Consumed',
            'Exp Year', 'Exp Month Start', 'Exp Month End',
            'Quantity', 'Duration', 'Adjustment Code',
        ]

        for activity in Activity.objects.all():

            date_filled = activity.date_filled
            if date_filled:
                date_filled = date_filled.strftime(self.date_format)
            else:
                date_filled = ''

            date_consumed = activity.date_consumed
            if date_consumed:
                date_consumed = date_consumed.strftime(self.date_format)
            else:
                date_consumed = ''

            row = [
                activity.box_number,
                activity.box_type,
                activity.loc_row,
                activity.loc_bin,
                activity.loc_tier,
                activity.prod_name,
                activity.prod_cat_name,
                date_filled,
                date_consumed,
                activity.exp_year,
                activity.exp_month_start,
                activity.exp_month_end,
                activity.quantity,
                activity.duration,
                activity.adjustment_code,
            ]
            yield row

    def get(self, request, *args, **kwargs):
        pseudo_buffer = self.Echo()
        writer = csv_writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in self.write_rows()),
            content_type="text/csv"
        )
        response['Content-Disposition'] = 'attachment; filename="activities.csv"'
        return response


class ManualBoxStatusView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.view_box',
    )

    template_name = 'fpiweb/manual_box_status.html'

    MODE_ENTER_BOX_NUMBER = 'enter_box_number'
    MODE_CONFIRMATION = 'confirmation'

    @staticmethod
    def build_context(
            *,
            mode,
            box_number_form=None,
            box=None,
            box_type=None,
            product_form=None,
            product=None,
            location_form=None,
            location=None,
            errors=None):
        return {
            'mode': mode,
            'box_number_form': box_number_form,
            'box': box,
            'box_type': box_type,
            'product_form': product_form,
            'product': product,
            'location_form': location_form,
            'location': location,
            'view_class': ManualBoxStatusView,
            'errors': errors,
        }

    def get(self, request, *args, **kwargs):
        """
        Prepare to display consume box number form for the first time.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        get_context = self.build_context(
            mode=self.MODE_ENTER_BOX_NUMBER,
            box_number_form=FilledBoxNumberForm(),
        )
        return render(request, self.template_name, get_context)

    def post_box_number(self, request):
        box_number_form = ExtantBoxNumberForm(request.POST)
        if not box_number_form.is_valid():
            box_number_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_NUMBER,
                box_number_form=box_number_form,
                errors=box_number_form.errors,
            )
            return render(
                request,
                self.template_name,
                box_number_failed_context,
                status=HTTPStatus.NOT_FOUND,
            )

        box_number = box_number_form.cleaned_data.get('box_number')
        # go get the final box info
        box = Box.objects.select_related(
            'box_type',
            'product',
            'location',
        ).get(box_number=box_number)
        box_type = box.box_type
        product = box.product
        location = box.location

        # go get the final box info after any modifications
        return render(
            request,
            self.template_name,
            self.build_context(
                mode=self.MODE_CONFIRMATION,
                box=box,
                box_type=box_type,
                product=product,
                location=location,
            ),
        )

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode')
        if mode == self.MODE_ENTER_BOX_NUMBER:
            return self.post_box_number(request)
        print(f"Unrecognized mode '{mode}'")
        return render(request, self.template_name, {})


class ManualNewBoxView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.add_box',
    )

    template_name = 'fpiweb/manual_new_box.html'

    MODE_ENTER_BOX_NUMBER = 'enter_box_number'
    MODE_CONFIRMATION = 'confirmation'

    @staticmethod
    def build_context(
            *,
            mode,
            box_number_form=None,
            box=None,
            box_type=None,
            box_type_form=None,
            errors: Optional[list]=None):
        return {
            'mode': mode,
            'box_number_form': box_number_form,
            'box': box,
            'box_type': box_type,
            'box_type_form': box_type_form,
            'view_class': ManualNewBoxView,
            'errors': errors,
        }

    def get(self, request, *args, **kwargs):
        """
        Prepare to display add new box number form for the first time.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        get_context = self.build_context(
            mode=self.MODE_ENTER_BOX_NUMBER,
            box_number_form=NewBoxNumberForm(),
            box_type_form=ExistingBoxTypeForm(),
        )
        return render(request, self.template_name, get_context)

    def post_box_number(self, request):
        box_number_form = NewBoxNumberForm(request.POST)
        box_type_form = ExistingBoxTypeForm(request.POST)
        if not box_number_form.is_valid():
            box_number = box_number_form.data['box_number']
            box_number_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_NUMBER,
                box_number_form=box_number_form,
                box_type_form=box_type_form,
                errors=[f"Box {box_number} already in inventory"],
            )
            return render(
                request,
                self.template_name,
                box_number_failed_context,
                status=HTTPStatus.NOT_FOUND,
            )

        box_number = box_number_form.cleaned_data.get('box_number')

        if not box_type_form.is_valid():
            box_type_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_NUMBER,
                box_number_form=box_number_form,
                box_type_form=box_type_form,
            )
            return render(
                request,
                self.template_name,
                box_type_failed_context,
                status=HTTPStatus.NOT_FOUND,
            )
        box_type = box_type_form.cleaned_data['box_type']

        # add the box to inventory
        box_mgmt = BoxManagementClass()
        box = box_mgmt.box_new(box_number=box_number, box_type=box_type)

        # present the final box info
        return render(
            request,
            self.template_name,
            self.build_context(
                mode=self.MODE_CONFIRMATION,
                box=box,
                box_type=box_type,
            ),
        )

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode')
        if mode == self.MODE_ENTER_BOX_NUMBER:
            return self.post_box_number(request)
        print(f"Unrecognized mode '{mode}'")
        return render(request, self.template_name, {})


class ManualCheckinBoxView(PermissionRequiredMixin, View):
    """ Manually check a box into inventory. """

    permission_required = (
        'fpiweb.check_in_box',
    )

    template_name = 'fpiweb/manual_check_in_box.html'

    MODE_ENTER_BOX_INFO = 'enter_box_info'
    MODE_CONFIRMATION = 'confirmation'

    @staticmethod
    def build_context(
            *,
            mode,
            box_number_form=None,
            box_number=None,
            box_form=None,
            box=None,
            product_form=None,
            product=None,
            location_form=None,
            location=None,
            exp_year_form=None,
            exp_year=None,
            exp_month_start_form=None,
            exp_month_start=None,
            exp_month_end_form=None,
            exp_month_end=None,
            errors: Optional[list]=None):
        return {
            'mode': mode,
            'box_number_form': box_number_form,
            'box_number': box_number,
            'box': box,
            'product_form': product_form,
            'product': product,
            'location_form': location_form,
            'location': location,
            'exp_year_form': exp_year_form,
            'exp_year': exp_year,
            'exp_month_start_form': exp_month_start_form,
            'exp_month_start': exp_month_start,
            'exp_month_end_form': exp_month_end_form,
            'exp_month_end': exp_month_end,
            'view_class': ManualCheckinBoxView,
            'errors': errors,
        }

    def get(self, request, *args, **kwargs):
        get_context = self.build_context(
            mode=self.MODE_ENTER_BOX_INFO,
            box_number_form=EmptyBoxNumberForm(),
            product_form=ExistingProductForm(),
            location_form=ExistingLocationForm(),
            exp_year_form=ExpYearForm(),
            exp_month_start_form=ExpMoStartForm(),
            exp_month_end_form=ExpMoEndForm(),
        )
        return render(request, self.template_name, get_context)

    def post_box_info(self, request):
        """
        Validate the posted information.

        :param request: container of initial or latest post
        :return:
        """
        # initialize variables that will be filled in later
        box_number = None
        box = None
        product = None
        location = None
        exp_year = None
        exp_month_start = None
        exp_month_end = None

        # start by hoping everything is ok -- then validate
        status = HTTPStatus.OK
        error_msgs = list()

        # validate box number
        box_number_form = ExtantBoxNumberForm(request.POST)
        if not box_number_form.is_valid():
            status = HTTPStatus.NOT_FOUND
            error_msgs.append(f'Invalid box number')
        else:
            box_number = box_number_form.cleaned_data.get('box_number')
            box = Box.objects.get(box_number=box_number)

        # Validate product
        product_form = ExistingProductForm(request.POST)
        if not product_form.is_valid():
            status = HTTPStatus.BAD_REQUEST
            error_msgs.append('Missing product')
        else:
            product = product_form.cleaned_data.get('product')

        # validate location
        location_form = ExistingLocationForm(request.POST)
        if not location_form.is_valid():
            status = HTTPStatus.BAD_REQUEST
            error_msgs.append('Missing location')
        else:
            location = location_form.cleaned_data.get('location')

        # validate expiration year
        exp_year_form = ExpYearForm(request.POST)
        if not exp_year_form.is_valid():
            status = HTTPStatus.BAD_REQUEST
            error_msgs.append('invalid expiration year')
        exp_year = exp_year_form.cleaned_data.get('exp_year')

        # validate expiration months
        exp_month_start_form = ExpMoStartForm(request.POST)
        exp_month_end_form = ExpMoEndForm(request.POST)

        if (not exp_month_start_form.is_valid()) or \
                (not exp_month_end_form.is_valid()):
            status = HTTPStatus.BAD_REQUEST
            error_msgs.append('invalid expiration month start')
        else:
            exp_month_start = exp_month_start_form.cleaned_data.get(
                'exp_month_start')

            exp_month_end = exp_month_end_form.cleaned_data.get(
                'exp_month_end')
            validation = validation_exp_months_bool(
                exp_month_start,
                exp_month_end
            )
            if not validation.is_valid:
                status = HTTPStatus.BAD_REQUEST
                error_msgs = error_msgs + validation.error_msg_list

        # Was everything valid?  If not, report it
        if status != HTTPStatus.OK:
            validation_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_INFO,
                box_number_form=box_number_form,
                product_form=product_form,
                location_form=location_form,
                exp_year_form=exp_year_form,
                exp_month_start_form=exp_month_start_form,
                exp_month_end_form=exp_month_end_form,
                errors=error_msgs,
            )
            return render(
                request,
                self.template_name,
                validation_failed_context,
                status=status
            )

        # apply fill box to database
        box_mgmt = BoxManagementClass()
        try:
            box = box_mgmt.box_fill(
                box=box,
                location=location,
                product=product,
                exp_year=exp_year,
                exp_mo_start=exp_month_start,
                exp_mo_end=exp_month_end,
        )
        except ProjectError as xcp:
            modify_box_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_INFO,
                box_number_form=box_number_form,
                box=box,
                product_form=product_form,
                product=product,
                location_form=location_form,
                location=location,
                # exp_month_start_form=exp_month_start_form,
                # exp_month_start=exp_month_start,
                # exp_month_end_form=exp_month_end_form,
                # exp_month_end=exp_month_end,
                errors=[xcp],
            )
            return render(
                request,
                self.template_name,
                modify_box_failed_context,
                status=HTTPStatus.BAD_REQUEST,
            )

        # go get box info for the final display
        # box_form = BoxItem()
        filled_box = Box.objects.select_related(
            'box_type',
            'product',
            'location',
        ).get(id=box.id)
        box_type = box.box_type
        product = box.product
        location = box.location
        return render(
            request,
            self.template_name,
            self.build_context(
                mode=self.MODE_CONFIRMATION,
                box=filled_box,
                product=product,
                location=location,
                exp_year=exp_year,
                exp_month_start=exp_month_start,
                exp_month_end=exp_month_end,
                errors=[],
            ),
        )

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode')
        if mode == self.MODE_ENTER_BOX_INFO:
            return self.post_box_info(request)
        print(f"Unrecognized mode '{mode}'")
        return render(request, self.template_name, {})


class ManualConsumeBoxView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.check_out_box',
    )

    template_name = 'fpiweb/manual_check_out_box.html'

    MODE_ENTER_BOX_NUMBER = 'enter_box_number'
    MODE_CONSUME_BOX = 'consume_box'
    MODE_CONFIRMATION = 'confirmation'

    @staticmethod
    def build_context(
            *,
            mode,
            box_number_form=None,
            box=None,
            box_type=None,
            product_form=None,
            product=None,
            location_form=None,
            location=None,
            errors: Optional[list]=None):
        return {
            'mode': mode,
            'box_number_form': box_number_form,
            'box': box,
            'box_type': box_type,
            'product_form': product_form,
            'product': product,
            'location_form': location_form,
            'location': location,
            'view_class': ManualConsumeBoxView,
            'errors': errors,
        }

    def get(self, request, *args, **kwargs):
        """
        Prepare to display consume box number form for the first time.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        get_context = self.build_context(
            mode=self.MODE_ENTER_BOX_NUMBER,
            box_number_form=FilledBoxNumberForm(),
        )
        return render(request, self.template_name, get_context)

    def post_box_number(self, request):
        box_number_form = FilledBoxNumberForm(request.POST)
        if not box_number_form.is_valid():
            box_number_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_NUMBER,
                box_number_form=box_number_form,
                errors=['Box number missing or box is empty']
            )
            return render(
                request,
                self.template_name,
                box_number_failed_context,
                status=HTTPStatus.BAD_REQUEST,
            )

        box_number = box_number_form.cleaned_data.get('box_number')
        # go get the final box info
        filled_box = Box.objects.select_related(
            'box_type',
            'product',
            'location',
        ).get(box_number=box_number)
        box_type = filled_box.box_type
        product = filled_box.product
        location = filled_box.location
        pre_consume_context = self.build_context(
            mode=self.MODE_CONSUME_BOX,
            box=filled_box,
            box_type=box_type,
            product=product,
            location=location,
        )
        return render(
            request,
            self.template_name,
            pre_consume_context,
        )

    def post_consume_box(self, request):
        box_pk = request.POST.get('box_pk')
        if not box_pk:
            box_failed_context = self.build_context(
                mode=self.MODE_ENTER_BOX_NUMBER,
                box_number_form=FilledBoxNumberForm(),
                errors=['Missing box_pk']
            ),
            return render(
                request,
                self.template_name,
                box_failed_context,
                status=HTTPStatus.BAD_REQUEST,
            )
        box = Box.objects.get(pk=box_pk)

        # apply box consumption to database
        box_mgmt = BoxManagementClass()
        box = box_mgmt.box_consume(box=box)

        # go get the final box info after any modifications
        empty_box = Box.objects.select_related(
            'box_type',
        ).get(id=box.id)
        box_type = box.box_type
        return render(
            request,
            self.template_name,
            self.build_context(
                mode=self.MODE_CONFIRMATION,
                box=empty_box,
                box_type=box_type,
            ),
        )

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode')
        if mode == self.MODE_ENTER_BOX_NUMBER:
            return self.post_box_number(request)
        if mode == self.MODE_CONSUME_BOX:
            return self.post_consume_box(request)
        print(f"Unrecognized mode '{mode}'")
        return render(request, self.template_name, {})


class ManualMoveBoxView(PermissionRequiredMixin, View):

    permission_required = (
        'fpiweb.move_box',
    )

    template_name = 'fpiweb/manual_move_box.html'

    MODE_ENTER_BOX_NUMBER = 'enter_box_number'
    MODE_ENTER_LOCATION = 'enter_location'
    MODE_CONFIRMATION = 'confirmation'

    @staticmethod
    def build_context(
            *,
            mode,
            box_number_form=None,
            box=None,
            location_form=None,
            errors: Optional[list]=None):
        return {
            'mode': mode,
            'box_number_form': box_number_form,
            'box': box,
            'location_form': location_form,
            'view_class': ManualMoveBoxView,
            'errors': errors,
        }

    def get(self, request, *args, **kwargs):
        context = self.build_context(
            mode=self.MODE_ENTER_BOX_NUMBER,
            box_number_form=FilledBoxNumberForm(),
        )
        return render(request, self.template_name, context)

    def post_box_number(self, request):
        box_number_form = FilledBoxNumberForm(request.POST)
        if not box_number_form.is_valid():
            context = self.build_context(
                mode=self.MODE_ENTER_BOX_NUMBER,
                box_number_form=box_number_form,
                errors=['Box number invalid']
            )
            return render(
                request,
                self.template_name,
                context,
                status=HTTPStatus.NOT_FOUND,
            )

        box_number = box_number_form.cleaned_data.get('box_number')

        boxes = Box.select_location(
            Box.objects.filter(box_number=box_number)
        )

        return render(
            request,
            self.template_name,
            self.build_context(
                mode=self.MODE_ENTER_LOCATION,
                box=boxes.first(),
                location_form=ExistingLocationForm(),
            )
        )

    def post_location(self, request):
        box_pk = request.POST.get('box_pk')
        if not box_pk:
            return render(
                request,
                self.template_name,
                self.build_context(
                    mode=self.MODE_ENTER_BOX_NUMBER,
                    errors=['Missing box_pk']
                ),
                status=HTTPStatus.BAD_REQUEST,
            )

        try:
            box = Box.objects.get(pk=box_pk)
        except Box.DoesNotExist as dne:
            message = str(dne)
            logger.error(message)
            return render(
                request,
                self.template_name,
                self.build_context(
                    mode=self.MODE_ENTER_BOX_NUMBER,
                    errors=[message]
                ),
                status=HTTPStatus.NOT_FOUND,
            )

        location_form = ExistingLocationForm(request.POST)
        if not location_form.is_valid():
            return render(
                request,
                self.template_name,
                self.build_context(
                    mode=self.MODE_ENTER_LOCATION,
                    box=box,
                    location_form=location_form,
                    errors=['invalid or missing location'],
                ),
                status=HTTPStatus.NOT_FOUND
            )

        location = location_form.cleaned_data.get('location')
        if not location:
            message = "Unable to retrieve location from form"
            logger.error(message)
            return render(
                request,
                self.template_name,
                self.build_context(
                    mode=self.MODE_ENTER_LOCATION,
                    box=box,
                    location_form=location_form,
                    errors=['invalid or missing location'],
                ),
                status=HTTPStatus.NOT_FOUND
            )

        # apply location change to database
        box_mgmt = BoxManagementClass()
        box = box_mgmt.box_move(
            box=box,
            location=location
        )

        return render(
            request,
            self.template_name,
            self.build_context(
                mode=self.MODE_CONFIRMATION,
                box=box,
            ),
        )

    def post(self, request, *args, **kwargs):
        mode = request.POST.get('mode')
        if mode == self.MODE_ENTER_BOX_NUMBER:
            return self.post_box_number(request)
        if mode == self.MODE_ENTER_LOCATION:
            return self.post_location(request)
        print(f"Unrecognized mode '{mode}'")
        return render(request, self.template_name, {})


class PalletManagementView(PermissionRequiredMixin, View):
    """Select current pallet, add new pallet, delete pallet"""

    permission_required = (
        'fpiweb.dummy_profile',
    )

    template_name = 'fpiweb/pallet_management.html'

    @staticmethod
    def show_page(
            request,
            page_title='Pallet Management',
            show_delete=True,
            prompt=None,
            pallet_select_form=None,
            pallet_name_form=None,
            status_code=HTTPStatus.OK):

        context = {
            'page_title': page_title,
            'show_delete': show_delete,
            'prompt': prompt,
            'pallet_select_form': pallet_select_form or PalletSelectForm(),
            'pallet_name_form': pallet_name_form or PalletNameForm(),
        }
        return render(
            request,
            PalletManagementView.template_name,
            context,
            status=status_code
        )

    def get(self, request):
        return self.show_page(request)


class PalletSelectView(PermissionRequiredMixin, FormView):

    permission_required = (
        'fpiweb.dummy_profile',
    )

    template_name = 'fpiweb/pallet_select.html'
    success_url = reverse_lazy('fpiweb:index')
    form_class = PalletSelectForm

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        pallet = form.cleaned_data['pallet']
        # set default status
        pallet.pallet_status = Pallet.FILL

        user, profile = get_user_and_profile(self.request)
        profile.active_pallet = pallet
        profile.save()

        return super().form_valid(form)

# EOF
