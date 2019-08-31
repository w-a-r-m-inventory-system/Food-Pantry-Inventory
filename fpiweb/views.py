"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from logging import getLogger, debug, info

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import \
    TemplateView, \
    ListView, \
    DetailView, \
    CreateView, \
    UpdateView, \
    DeleteView, \
    FormView

from fpiweb.models import \
    Action, \
    Box, \
    BoxNumber, \
    Constraints, \
    LocRow, \
    LocBin, \
    LocTier
from fpiweb.forms import \
    BoxItemForm, \
    BuildPalletForm, \
    ConstraintsForm, \
    LoginForm, \
    LocRowForm, \
    LocBinForm, \
    LocTierForm, \
    NewBoxForm

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

    formClass = ConstraintsForm

    # TODO Why are fields required here in the create - 1/18/17
    fields = ['constraint_name', 'constraint_descr', 'constraint_type',
              'constraint_min', 'constraint_max', 'constraint_list', ]

    def get_success_url(self):
        """
        Run once form is successfully validated.

        :return:
        """
        results = reverse('fpiweb:constraints_view')
        return results


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

        action = request.session.get('action')
        if action == Action.ACTION_BUILD_PALLET:
            return redirect(
                reverse(
                    'fpiweb:build_pallet_add_box',
                    args=(box.pk,)
                )
            )

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

        action = request.session.get('action')

        if action != Action.ACTION_BUILD_PALLET:
            return error_page(
                request,
                "What to do when action is {}?".format(action)
            )

        try:
            box = Box.objects.get(box_number=box_number)
        except Box.DoesNotExist:
            return redirect('fpiweb:box_new', box_number=box_number)

        return redirect('fpiweb:build_pallet_add_box', args=(box.pk,))


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
    template_name = 'fpiweb/build_pallet.html'

    BoxFormFactory = modelformset_factory(
        Box,
        form=BoxItemForm,
        extra=0,
    )

    def get(self, request, *args, **kwargs):

        request.session['action'] = Action.ACTION_BUILD_PALLET

        box_pk = kwargs.get('box_pk')

        build_pallet_form = BuildPalletForm()

        kwargs = {
            'prefix': 'box_forms',
        }
        if box_pk:
            kwargs['queryset'] = Box.objects.filter(pk=box_pk)
        else:
            kwargs['queryset'] = Box.objects.none()

        box_forms = self.BoxFormFactory(**kwargs)

        context = {
            'form': build_pallet_form,
            'box_forms': box_forms,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = BuildPalletForm(request.POST)
        box_forms = self.BoxFormFactory(request.POST, prefix='box_forms')

        if box_forms and len(box_forms) > 0:
            box_form = box_forms[0]
            print(dir(box_form))

        if not form.is_valid() or not box_forms.is_valid():
            return render(
                request,
                self.template_name,
                {
                    'form': form,
                    'box_forms': box_forms,
                }
            )

        return error_page(request, "forms are valid")

# EOF
