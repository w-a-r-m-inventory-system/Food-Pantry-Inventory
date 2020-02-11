"""
views.py - establish the views (pages) for the F. P. I. web application.
"""

from collections import OrderedDict
from csv import writer as csv_writer
from enum import Enum
from io import BytesIO
from json import loads
from logging import getLogger, debug, info
from string import digits
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Max
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
    ExtantBoxNumberForm, \
    BuildPalletForm, \
    ConstraintsForm, \
    ExistingLocationForm, \
    LocRowForm, \
    LocBinForm, \
    LocTierForm, \
    LoginForm, \
    NewBoxForm, \
    PalletNameForm, \
    PalletSelectForm, \
    PrintLabelsForm
from fpiweb.qr_code_utilities import QRCodePrinter
from fpiweb.support.BoxActivity import BoxActivityClass
from fpiweb.support.BoxManagement import BoxManagementClass

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

logger = getLogger('fpiweb')


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


def get_user_and_profile(request):
    user = request.user
    profile = user.profile or Profile.objects.create(user=user)
    return user, profile


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
    context_object_name = 'about_context'

    def get_context_data(self, **kwargs):
        """
        Add Site Information to About page.

        :param kwargs:
        :return:
        """

        # get this information from the database later
        context = super(AboutView, self).get_context_data(**kwargs)
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


class MaintenanceView(LoginRequiredMixin, TemplateView):
    """
    Default web page (/index)
    """
    template_name = 'fpiweb/maintenance.html'


class LocRowListView(LoginRequiredMixin, ListView):
    """
    List of existing rows using a generic ListView.
    """

    model = LocRow
    template_name = 'fpiweb/loc_row_list.html'
    context_object_name = 'loc_row_list_content'


class LocRowCreateView(LoginRequiredMixin, CreateView):
    """
    Create a row using a generic CreateView.
    """

    model = LocRow
    template_name = 'fpiweb/loc_row_edit.html'
    context_object_name = 'loc_row'
    success_url = reverse_lazy('fpiweb:loc_row_view')

    formClass = LocRowForm

    fields = ['loc_row', 'loc_row_descr', ]


class LocRowUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a row using a generic UpdateView.
    """

    model = LocRow
    template_name = 'fpiweb/loc_row_edit.html'
    context_object_name = 'loc_row'
    form_class = LocRowForm
    success_url = reverse_lazy('fpiweb:loc_row_view')


class LocRowDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a row using a generic DeleteView.
    """

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


class LocBinListView(LoginRequiredMixin, ListView):
    """
    List of existing bins using a generic ListView.
    """

    model = LocBin
    template_name = 'fpiweb/loc_bin_list.html'
    context_object_name = 'loc_bin_list_content'


class LocBinCreateView(LoginRequiredMixin, CreateView):
    """
    Create a bin using a generic CreateView.
    """

    model = LocBin
    template_name = 'fpiweb/loc_bin_edit.html'
    context_object_name = 'loc_bin'
    success_url = reverse_lazy('fpiweb:loc_bin_view')

    formClass = LocBinForm

    fields = ['loc_bin', 'loc_bin_descr', ]


class LocBinUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a bin using a generic UpdateView.
    """

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


class LocBinDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a bin using a generic DeleteView.
    """

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


class LocTierListView(LoginRequiredMixin, ListView):
    """
    List of existing tiers using a generic ListView.
    """

    model = LocTier
    template_name = 'fpiweb/loc_tier_list.html'
    context_object_name = 'loc_tier_list_content'


class LocTierCreateView(LoginRequiredMixin, CreateView):
    """
    Create a tier using a generic CreateView.
    """

    model = LocTier
    template_name = 'fpiweb/loc_tier_edit.html'
    context_object_name = 'loc_tier'
    success_url = reverse_lazy('fpiweb:loc_tier_view')

    formClass = LocTierForm

    fields = ['loc_tier', 'loc_tier_descr', ]


class LocTierUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a tier using a generic UpdateView.
    """

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


class LocTierDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a tier using a generic DeleteView.
    """

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
        info(
            f'Constraint extra info: INT_RANGE: {INT_RANGE}, '
            f'CHAR__RANGE: '
            f'{CHAR_RANGE}, range_list: {range_list}'
        )

        return context


class ConstraintCreateView(LoginRequiredMixin, CreateView):
    """
    Create a constraint using a generic CreateView.
    """

    model = Constraints
    template_name = 'fpiweb/constraint_edit.html'
    context_object_name = 'constraints'
    success_url = reverse_lazy('fpiweb:constraints_view')

    formClass = ConstraintsForm

    # TODO Why are fields required here in the create - 1/18/17
    fields = ['constraint_name', 'constraint_descr', 'constraint_type',
              'constraint_min', 'constraint_max', 'constraint_list', ]


class ConstraintUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update a constraint using a generic UpdateView.
    """

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


class ConstraintDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a constraint using a generic DeleteView.
    """

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
    template_name = 'fpiweb/box_empty_move.html'

    def get_context_data(self, **kwargs):
        return {}


class BoxEmptyView(LoginRequiredMixin, View):
    pass


class BoxScannedView(LoginRequiredMixin, View):

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


class BuildPalletView(View):
    """Set action in view"""

    form_template = 'fpiweb/build_pallet.html'
    confirmation_template = 'fpiweb/build_pallet_confirmation.html'
    formset_prefix = 'box_forms'
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
            pallet,
            status=400):
        """
        Display page with BuildPalletForm and BoxItemForms
        :param request:
        :param build_pallet_form:
        :param box_forms:
        :param status:
        :return:
        """

        return render(
            request,
            self.form_template,
            {
                'form': build_pallet_form,
                'box_forms': box_forms,
                'pallet': pallet,
            },
            status=status,
        )

    @staticmethod
    def show_pallet_management_page(
            request,
            pallet_select_form=None,
            pallet_name_form=None):

        return PalletManagementView.show_page(
            request,
            page_title=BuildPalletView.page_title,
            prompt="Select an existing pallet or create a new one to continue",
            show_delete=False,
            pallet_select_form=pallet_select_form,
            pallet_name_form=pallet_name_form,
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
            return self.process_build_pallet_forms(request)

        if form_name not in [
                self.PALLET_SELECT_FORM_NAME,
                self.PALLET_NAME_FORM_NAME]:
            message = f"Unexpected form name {repr(form_name)}"
            logger.error(message)
            return error_page(
                request,
                message=message,
                status=500
            )

        pallet = None
        if form_name == self.PALLET_SELECT_FORM_NAME:
            pallet_select_form = PalletSelectForm(request.POST)
            if not pallet_select_form.is_valid():
                return self.show_pallet_management_page(
                    request,
                    pallet_select_form=pallet_select_form,
                )
            pallet = pallet_select_form.cleaned_data.get('pallet')

        if form_name == self.PALLET_NAME_FORM_NAME:
            pallet_name_form = PalletNameForm(request.POST)
            if not pallet_name_form.is_valid():
                return self.show_pallet_management_page(
                    request,
                    pallet_name_form=pallet_name_form,
                )
            pallet = pallet_name_form.save()

        if not pallet:
            message = f"pallet not set"
            logger.error(message)
            return error_page(
                request,
                message=message,
                status=500,
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

        build_pallet_form = BuildPalletForm(instance=pallet.location)

        box_forms = self.BoxFormFactory(
            initial=initial_data,
            prefix=self.formset_prefix,
        )

        return self.show_forms_response(
            request,
            build_pallet_form,
            box_forms,
            pallet,
            status=200,
        )

    def process_build_pallet_forms(self, request):

        build_pallet_form = BuildPalletForm(request.POST)
        box_forms = self.BoxFormFactory(
            request.POST,
            prefix=self.formset_prefix,
        )

        build_pallet_form_valid = build_pallet_form.is_valid()
        if not build_pallet_form_valid:
            logger.debug("BuildPalletForm not valid")

        box_forms_valid = box_forms.is_valid()
        if not box_forms_valid:
            logger.debug("BoxForms not valid")

        if not all([build_pallet_form_valid, box_forms_valid]):
            return self.show_forms_response(
                request,
                build_pallet_form,
                box_forms,
            )

        location = build_pallet_form.instance

        # Update box records and
        boxes_by_box_number = OrderedDict()
        duplicate_box_numbers = set()
        forms_missing_box_number = 0
        for i, box_form in enumerate(box_forms):
            cleaned_data = box_form.cleaned_data
            if not cleaned_data:
                continue

            box_number = cleaned_data.get('box_number')
            if not isinstance(box_number, str):
                logger.error(f"box_number {box_number} is a {type(box_number)}")
                continue

            # Is this a duplicate box_id?
            if box_number in boxes_by_box_number:
                duplicate_box_numbers.add(box_number)
                continue

            # Is box_number present in database?
            try:
                box = Box.objects.get(box_number=box_number)
                logger.debug(f"found existing box {box_number}")
            except Box.DoesNotExist:
                box = Box(
                    box_number=box_number,
                    box_type=Box.box_type_default(),
                )
                logger.debug(f"Created new box {box_number}")

            boxes_by_box_number[box_number] = box

            if box.is_filled():
                box_management = BoxManagementClass()
                box_management.box_consume(box)

            box.product = cleaned_data.get('product')
            box.exp_year = cleaned_data.get('exp_year')
            box.exp_month_start = cleaned_data.get('exp_month_start')
            box.exp_month_end = cleaned_data.get('exp_month_end')
            box.save()

            box_management.box_move(box, location)

        if forms_missing_box_number > 0:
            # error reported on box_form
            logger.debug("forms_missing_box_number > 0")
            return self.show_forms_response(
                request,
                build_pallet_form,
                box_forms,
            )

        if duplicate_box_numbers:
            duplicate_box_numbers = [str(k) for k in duplicate_box_numbers]
            message = f"Duplicate box numbers: {', '.join(duplicate_box_numbers)}"
            logger.debug(message)
            build_pallet_form.add_error(None, message)
            return self.show_forms_response(
                request,
                build_pallet_form,
                box_forms,
            )

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


class ScannerView(View):

    @staticmethod
    def response(success, data=None, errors=None, status=200):
        return JsonResponse(
            {
                'success': success,
                'data': data if data else {},
                'errors': errors if errors else [],
            },
            status=status
        )

    @staticmethod
    def error_response(errors, status=400):
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

    def post(self, request):

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

        return self.response(True, data=box_data, status=200)


class PrintLabelsView(View):

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

        QRCodePrinter().print(
            form.cleaned_data.get('starting_number'),
            form.cleaned_data.get('number_to_print'),
            buffer,
        )

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='labels.pdf')


class BoxItemFormView(LoginRequiredMixin, View):

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
            return HttpResponse("Scan failed.", status=404)

        try:
            pallet = Pallet.objects.get(pk=pallet_pk)
        except Pallet.DoesNotExist as dne:
            error = str(dne)
            logger.error(error)
            return HttpResponse(f"Pallet pk={pallet_pk} not found", status=404)

        # If box is filled, empty it before continuing
        if box.is_filled():
            box_management = BoxManagementClass()
            box_management.box_consume(box)

        # Look for PalletBox record
        pallet_box, created = PalletBox.objects.get_or_create(
            box_number=box.box_number,
            pallet=pallet
        )

        return render(
            request,
            self.template_name,
            {
                'box_number': box.box_number,
                'form': self.get_form(pallet_box, prefix),
            },
        )


class ManualMenuView(TemplateView):
    """
    Default web page (/index)
    """
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
            pallet_target = reverse_lazy(
                'fpiweb:manual_pallet_status', args=[active_pallet.id]
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

    def get_success_url(self, **kwargs):
        """
        Construct success url.

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
        status: int = 200):
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

    # content_type: use default
    # status: 200 = OK, 400 = Bad Request, 418 = I am a teapot
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


class ManualPalletStatus(LoginRequiredMixin, ListView):
    """
    Establish a new pallet for this user.
    """

    model = Pallet
    template_name = 'fpiweb/manual_pallet_status.html'
    context_object_name = 'manual_pallet_status'
    success_url = reverse_lazy('fpiweb:manual_menu')

    def get_context_data(self, **kwargs):
        """
        Add Site Information to About page.

        :param kwargs:
        :return:
        """

        # get stuff from the request
        context = super(ManualPalletStatus, self).get_context_data(**kwargs)

        # get related stuff from the database
        pallet_rec = context['manual_pallet_status'].get()
        pallet_user_id = pallet_rec.user_id_id
        profile_rec = Profile.objects.get(user_id=pallet_user_id)
        active_location_id = profile_rec.active_location_id
        location_rec = Location.objects.get(id=active_location_id)
        location_row_id = location_rec.loc_row.id
        row_descr = location_rec.loc_row.loc_row_descr
        location_bin_id = location_rec.loc_bin.id
        bin_descr = location_rec.loc_bin.loc_bin_descr
        location_tier_id = location_rec.loc_tier.id
        tier_descr = location_rec.loc_tier.loc_tier_descr
        box_set = PalletBox.objects.filter(
            pallet_id_id=pallet_rec.id).order_by('box_number')

        # pallet_context = context['manual_pallet_status']
        # pallet_query = pallet_context.query
        warehouse_flag = location_rec.loc_in_warehouse
        # remove entires below before production
        context['warehouse_flag'] = warehouse_flag
        context['row_id'] = location_row_id
        context['row_descr'] = row_descr
        context['bin_id'] = location_bin_id
        context['bin_descr'] = bin_descr
        context['tier_id'] = location_tier_id
        context['tier_descr'] = tier_descr
        context['box_set'] = box_set
        return context


class ActivityDownloadView(LoginRequiredMixin, View):

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


class ManualMoveBoxView(LoginRequiredMixin, View):
    template_name = 'fpiweb/manual_move_box.html'

    MODE_ENTER_BOX_NUMBER = 'enter_box_number'
    MODE_ENTER_LOCATION = 'enter_location'
    MODE_CONFIRMATION = 'confirmation'

    @staticmethod
    def build_context(
            mode,
            box_number_form=None,
            box=None,
            location_form=None,
            errors=None):
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
            self.MODE_ENTER_BOX_NUMBER,
            ExtantBoxNumberForm(),
        )
        return render(request, self.template_name, context)

    def post_box_number(self, request):
        box_number_form = ExtantBoxNumberForm(request.POST)
        if not box_number_form.is_valid():
            context = self.build_context(
                self.MODE_ENTER_BOX_NUMBER,
                box_number_form,
            )
            return render(
                request,
                self.template_name,
                context,
                status=404,
            )

        box_number = box_number_form.cleaned_data.get('box_number')

        boxes = Box.select_location(
            Box.objects.filter(box_number=box_number)
        )

        return render(
            request,
            self.template_name,
            self.build_context(
                self.MODE_ENTER_LOCATION,
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
                    self.MODE_ENTER_BOX_NUMBER,
                    errors=['Missing box_pk']
                ),
                status=400,
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
                    self.MODE_ENTER_BOX_NUMBER,
                    errors=[message]
                ),
                status=404,
            )

        location_form = ExistingLocationForm(request.POST)
        if not location_form.is_valid():
            return render(
                request,
                self.template_name,
                self.build_context(
                    self.MODE_ENTER_LOCATION,
                    box=box,
                    location_form=location_form,
                ),
            )

        location = location_form.cleaned_data.get('location')
        if not location:
            message = "Unable to retrieve location from form"
            logger.error(message)
            return render(
                render,
                self.template_name
            )

        box.location = location
        box.save()

        box_activity = BoxActivityClass()
        box_activity.box_move(box_pk)

        return render(
            request,
            self.template_name,
            self.build_context(
                self.MODE_CONFIRMATION,
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


class PalletManagementView(LoginRequiredMixin, View):
    """Select current pallet, add new pallet, delete pallet"""

    template_name = 'fpiweb/pallet_management.html'

    @staticmethod
    def show_page(
            request,
            page_title='Pallet Management',
            show_delete=True,
            prompt=None,
            pallet_select_form=None,
            pallet_name_form=None):

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
            context
        )

    def get(self, request):
        return self.show_page(request)



# TODO: Might be able to convert this into FormView
class PalletSelectView(LoginRequiredMixin, FormView):

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

        user, profile = get_user_and_profile(self.request)
        profile.active_pallet = pallet
        profile.save()

        return super().form_valid(form)







# EOF
