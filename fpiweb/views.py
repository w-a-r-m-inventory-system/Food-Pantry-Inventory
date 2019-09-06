"""
views.py - establish the views (pages) for the F. P. I. web application.
"""
from base64 import b64decode
from binascii import Error as BinasciiError
from datetime import datetime
from io import BytesIO
from json import loads
from logging import getLogger, debug
from pathlib import Path
from random import seed, randint
from subprocess import CalledProcessError, run
from time import time

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Max
from django.forms import modelformset_factory
from django.http import FileResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, \
    CreateView, UpdateView, DeleteView, FormView

from fpiweb.models import \
    Action, \
    Box, \
    BoxNumber, \
    Constraints
from fpiweb.forms import \
    BoxItemForm, \
    BuildPalletForm, \
    ConstraintsForm, \
    LoginForm, \
    NewBoxForm, \
    PrintLabelsForm
from fpiweb.qr_code_utilities import QRCodePrinter

__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"


logger = getLogger('fpiweb')

seed(time())


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
        if settings.DEBUG == False and hasattr(self.request, 'schema'):
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

        if box_forms:
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
    def get_scan_file_path():
        scans_dir_path = Path(settings.SCANS_DIR)
        if not scans_dir_path.exists():
            raise OSError("{} doesn't exist".format(scans_dir_path))

        attempts = 100
        for i in range(attempts):
            filename = "{}_{:0>4}.png".format(
                datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                randint(0, 9999),
            )
            path = scans_dir_path / filename
            if not path.exists():
                return path
        raise OSError(
            "Unable to generate path after {} attempts".format(attempts)
        )

    def post(self, request, *args, **kwargs):
        print("ScannerView.post")
        scan_data_prefix = 'data:image/png;base64,'
        scan_data = request.POST.get('scanData')

        if not scan_data:
            error_message = 'missing scan_data'
            logger.error(error_message)
            return self.error_response([error_message])

        if not scan_data.startswith(scan_data_prefix):
            return self.error_response(['Invalid scan data'])

        logger.info("scan_data is {:,} characters in length".format(len(scan_data)))

        try:
            scan_data_bytes = b64decode(
                scan_data[len(scan_data_prefix):]
            )
        except BinasciiError as e:
            return self.error_response([str(e)])

        try:
            image_file_path = self.get_scan_file_path()
        except OSError as e:
            return self.error_response([str(e)])

        with image_file_path.open('wb') as image_file:
            image_file.write(scan_data_bytes)

        program_name = 'zbarimg'
        try:
            completed_process = run(
                [program_name, str(image_file_path)],
                capture_output=True,
                timeout=5,  # 5 seconds to run
            )
        except FileNotFoundError as error:
            error_message = str(error)
            logger.error(error_message)
            if program_name in error_message:
                logger.error(
                    error_message +
                    ".  Is the zbar-tools package installed.  "
                    "Use sudo apt-get install zbar-tools to install it.")
            return self.error_response([error_message])
        except RuntimeError as error:
            logger.error(error)
            return self.error_response([
                str(error),
                "error is a {}".format(type(error))
            ])

        if completed_process.returncode != 0:
            error_message = completed_process.stderr.decode()
            logger.error(error_message)
            return self.error_response([error_message])

        qr_data = completed_process.stdout.decode()
        match = BoxNumber.box_number_search_regex.search(qr_data)
        if not match:
            error_message = f"box number not found in {qr_data}"
            logger.error(error_message)
            return self.error_response([error_message])

        box_number = match.group().upper()
        logger.info(f"scanned box_number is {box_number}")

        box, created = Box.objects.get_or_create(
            box_number=box_number,
            defaults={
                'box_type': Box.box_type_default(),
            }
        )

        # serialize works on an iterable of objects and returns a string
        box_json = loads(serialize("json", [box]))

        # pull dict from list
        box_json = box_json[0]

        data = {
            'box': box_json,
            'box_meta': {
                'is_new': created,
            }
        }

        return self.response(True, data=data, status=200)


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

# EOF
