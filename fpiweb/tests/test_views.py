
__author__ = '(Multiple)'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/01/2019"

from bs4 import BeautifulSoup
from datetime import date

from django.contrib.auth.models import User
from django.forms.formsets import BaseFormSet
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.html import escape


from fpiweb.forms import \
    BuildPalletForm, \
    ConfirmMergeForm, \
    ExtantBoxNumberForm, \
    ExistingLocationForm, \
    ExistingLocationWithBoxesForm, \
    FilledBoxNumberForm, \
    HiddenPalletForm, \
    MoveToLocationForm, \
    PalletNameForm, \
    PalletSelectForm

from fpiweb.models import \
    Box, \
    BoxNumber, \
    BoxType, \
    Location, \
    LocRow, \
    LocBin, \
    LocTier, \
    Pallet, \
    PalletBox, \
    Product, \
    Activity, \
    Profile
from fpiweb.tests.utility import \
    create_user, \
    default_password, \
    logged_in_user
from fpiweb.views import \
    BoxItemFormView, \
    BuildPalletView, \
    ManualMoveBoxView, \
    ManualPalletMoveView


def management_form_post_data(
        prefix,
        total_forms,
        initial_forms=0,
        min_num_forms=0,
        max_num_forms=100):
    post_data = {
        'TOTAL_FORMS': total_forms,
        'INITIAL_FORMS': initial_forms,
        'MIN_NUM_FORMS': min_num_forms,
        'MAX_NUM_FORMS': max_num_forms,
    }
    return {f'{prefix}-{k}': v for k, v in post_data.items()}


def formset_form_post_data(prefix, form_index, form_data):
    form_data_out = {}
    for key, value in form_data.items():
        key = f'{prefix}-{form_index}-{key}'
        form_data_out[key] = value
    return form_data_out


class BoxNewViewTest(TestCase):

    # The second time I ran this test I got the following error:
    #
    # ...
    #       min_value, max_value = Constraints.get_values(constraint_name)
    # TypeError: cannot unpack non-iterable NoneType object
    #
    # [Translation: We don't have any Constraint records in the database, so
    # fixture time]
    #
    # Fixtures are files located in fpiweb/fixtures, you don't need to include
    # the .json part of the filename.  Note: if you have a tuple with only 1
    # item in it [ i.e. ('foo', ) ] the trailing comma is important.  With it
    # it's a 1 item tuple, without it's a expression with a redundant set of
    # parenthesis around it.  PyCharm will complain about the redundant
    # parenthesis.
    fixtures = ('Constraints', 'BoxType')

    def test_get_success_url(self):

        # create user for this test (It will only exist briefly in the test
        # database).
        # create an associated profile - just for the test
        user = User.objects.create_user(
            'awesterville',
            'alice.westerville@example.com',
            'abc123')
        profile = Profile.objects.create(
            title='Test User',
            user=user,
        )

        # Client sends HTTP requests and receives HTTP responses like a user's
        # browser.  It doesn't run any JavaScript, for that you need to use
        # Selenium to control a real browser.
        client = Client()

        # The first time I ran this test, I found that response.url was the
        # login page.  Ooops, forgot to log in.  Call the force_login method
        # to make Django act like we've gone through the login page
        client.force_login(user)

        box_number = BoxNumber.format_box_number(1)
        url = reverse('fpiweb:box_new', args=(box_number,))

        box_type = BoxType.objects.get(box_type_code='Evans')

        post_data = {
            'box_number': box_number,
            'box_type': box_type.pk,
        }

        response = client.post(url, post_data)

        # Check whether the HTTP status code is 200, if it's not display the
        # text of the page returned.  Sometimes this makes looking for what
        # happened like looking for a needle in a haystack.

        # Unit-testing frameworks like unittest or pytest may discard text
        # sent to the terminal (stdout) unless a test fails.
        # print(dir(response))

        # Here's a handy page to bookmark:
        #     https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        #
        # Status code 418 is my favorite!
        self.assertEqual(302, response.status_code, str(response.content))

        box = Box.objects.order_by('-pk').first()
        self.assertEqual(
            reverse('fpiweb:box_details', args=(box.pk,)),
            response.url
        )

        box = Box.objects.get(box_number=box_number)

        self.assertEqual(box_type, box.box_type)
        self.assertEqual(box_type.box_type_qty, box.quantity)


class IndexViewTest(TestCase):

    # fixtures = ('Profile',)

    def test_get_success_url(self):

        # create user for this test (It will only exist briefly in the test
        # database).
        # create an associated profile - just for the test
        user = User.objects.create_user(
            'awesterville',
            'alice.westerville@example.com',
            'abc123')
        profile = Profile.objects.create(
            title='Test User',
            user=user,
        )
        # Client sends HTTP requests and receives HTTP responses like a user's
        # browser.  It doesn't run any JavaScript, for that you need to use
        # Selenium to control a real browser.
        client = Client()

        # The first time I ran this test, I found that response.url was the
        # login page.  Ooops, forgot to log in.  Call the force_login method
        # to make Django act like we've gone through the login page
        client.force_login(user)

    # def test_get(self):
    #     client = Client()
        response = client.get(reverse('fpiweb:index'))
        self.assertEqual(200, response.status_code)


class AboutViewTest(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:about'))
        self.assertEqual(200, response.status_code)


class LoginViewTest(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:login'))
        self.assertEqual(200, response.status_code)

    def test_post(self):
        username = 'jdoe'
        password = 'abc123'
        User.objects.create_user(username, 'jdoe@example.com', password)

        client = Client()
        url = reverse('fpiweb:login')

        response = client.post(
            url,
            {
                'username': username,
                'password': password,
            },
        )

        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('fpiweb:index'), response.url)

        response = client.post(
            url,
            {
                'username': username,
                'password': 'NARF!!',
            },
        )

        # yeah, FormViews like this one return 200 status code if form
        # fails validation
        self.assertEqual(200, response.status_code)

        soup = BeautifulSoup(response.content, 'html.parser')
        error_list = soup.find('ul', class_='errorlist')
        self.assertIsNotNone(error_list)
        self.assertIn(
            "Invalid username and/or password",
            error_list.get_text(),
        )

    def test_login_required_redirects_to_login_view(self):
        client = Client()
        response = client.get(reverse('fpiweb:maintenance'))
        self.assertEqual(302, response.status_code)
        self.assertTrue(response.url.startswith(reverse('fpiweb:login')))


class LogoutViewTest(TestCase):

    def test_get(self):
        client = Client()
        response = client.get(reverse('fpiweb:logout'))
        self.assertEqual(200, response.status_code)


class BuildPalletViewTest(TestCase):

    fixtures = (
        'Location',
        'LocRow',
        'LocBin',
        'LocTier',
        'Product',
        'ProductCategory',
        'BoxType',
        'Constraints',
    )

    url = reverse_lazy('fpiweb:build_pallet')

    @staticmethod
    def get_build_pallet_form_post_data(location):
        post_data = {
            'loc_row': location.loc_row.pk,
            'loc_bin': location.loc_bin.pk,
            'loc_tier': location.loc_tier.pk,
        }
        prefix = BuildPalletView.build_pallet_form_prefix
        post_data = {f"{prefix}-{k}": v for k, v in post_data.items()}
        return post_data

    @staticmethod
    def build_boxes(number_of_boxes):
        boxes = []
        default_box_type = Box.box_type_default()
        for i in range(number_of_boxes):
            box_number = BoxNumber.get_next_box_number()
            box = Box.objects.create(
                box_number=box_number,
                box_type=default_box_type,
            )
            boxes.append(box)
        return boxes

    @staticmethod
    def build_pallet_boxes(pallet, boxes, product, exp_year):
        pallet_boxes = []
        for box in boxes:
            pallet_box = PalletBox(
                pallet=pallet,
                box=box,
                product=product,
                exp_year=exp_year,
            )
            pallet_boxes.append(pallet_box)
        return pallet_boxes

    @staticmethod
    def get_box_forms_post_data(pallet_boxes):
        prefix = BuildPalletView.formset_prefix
        post_data = management_form_post_data(
            prefix,
            len(pallet_boxes),
        )

        for i, pallet_box in enumerate(pallet_boxes):
            box = pallet_box.box
            form_data = {
                'id': box.id,
                'box_number': box.box_number,
                'product': pallet_box.product.id,
                'exp_year': pallet_box.exp_year,
            }

            if pallet_box.exp_month_start:
                form_data['exp_month_start'] = pallet_box.exp_month_start
            if pallet_box.exp_month_end:
                form_data['exp_month_end'] = pallet_box.exp_month_end

            form_data = formset_form_post_data(prefix, i, form_data)
            post_data.update(form_data)

        return post_data

    @staticmethod
    def get_hidden_pallet_form_post_data(pallet):
        key = f"{BuildPalletView.hidden_pallet_form_prefix}-pallet"
        return {key: pallet.pk}

    def test_get(self):

        user = create_user('bob', 'shrock')

        client = Client()
        client.force_login(user)

        response = client.get(self.url)
        self.assertEqual(200, response.status_code)

        pallet_select_form = response.context.get('pallet_select_form')
        self.assertIsInstance(pallet_select_form, PalletSelectForm)

        pallet_name_form = response.context.get('pallet_name_form')
        self.assertIsInstance(pallet_name_form, PalletNameForm)

    def test_post_bad_form_name(self):

        user = create_user('cindy', 'state')

        client = Client()
        client.force_login(user)

        form_name = 'cindy'
        response = client.post(
            self.url,
            {
                'form_name': form_name,
            }
        )
        self.assertContains(
            response,
            escape(f"Unexpected form name {repr(form_name)}"),
            status_code=500,
            html=True,
        )

    def test_post_pallet_select_name_form(self):

        user = create_user('alice', 'shrock')

        client = Client()
        client.force_login(user)

        # -------------------
        # No pallet selected
        # -------------------
        response = client.post(
            self.url,
            {
                'form_name': BuildPalletView.PALLET_SELECT_FORM_NAME,
            }
        )
        self.assertEqual(
            400,
            response.status_code,
            response.content.decode(),
        )
        self.assertIsInstance(
            response.context.get('pallet_select_form'),
            PalletSelectForm,
        )

        pallet = Pallet.objects.create()

        response = client.post(
            self.url,
            {
                'form_name': BuildPalletView.PALLET_SELECT_FORM_NAME,
                'pallet': pallet.pk
            }
        )
        self.assertEqual(200, response.status_code)

        build_pallet_form = response.context.get('form')
        box_forms = response.context.get('box_forms')
        pallet_form = response.context.get('pallet_form')

        self.assertIsInstance(build_pallet_form, BuildPalletForm)
        self.assertIsInstance(box_forms, BaseFormSet)
        self.assertIsInstance(pallet_form, HiddenPalletForm)

        pallet_form = response.context.get('pallet_form')
        self.assertIsInstance(pallet_form, HiddenPalletForm)
        self.assertEqual(
            pallet,
            pallet_form.initial.get('pallet')
        )

    def test_post_pallet_name_form(self):

        user = create_user('doug', 'state')

        client = Client()
        client.force_login(user)

        # -----------------------
        # No pallet name entered
        # -----------------------
        response = client.post(
            self.url,
            {
                'form_name': BuildPalletView.PALLET_NAME_FORM_NAME,
            }
        )
        self.assertEqual(400, response.status_code)
        self.assertIsInstance(
            response.context.get('pallet_name_form'),
            PalletNameForm,
        )

        pallet_name = "nuevo palet"
        response = client.post(
            self.url,
            {
                'form_name': BuildPalletView.PALLET_NAME_FORM_NAME,
                'name': pallet_name,
            }
        )
        self.assertEqual(200, response.status_code)

        build_pallet_form = response.context.get('form')
        box_forms = response.context.get('box_forms')
        pallet_form = response.context.get('pallet_form')

        self.assertIsInstance(build_pallet_form, BuildPalletForm)
        self.assertIsInstance(box_forms, BaseFormSet)
        self.assertIsInstance(pallet_form, HiddenPalletForm)

        pallet_form = response.context.get('pallet_form')
        self.assertIsInstance(pallet_form, HiddenPalletForm)
        self.assertEqual(
            Pallet.objects.get(name=pallet_name),
            pallet_form.initial.get('pallet'),
        )

    def test_post_process_box_forms(self):

        # Pick a specific Location
        location = Location.objects.get(
            loc_row__loc_row='01',
            loc_bin__loc_bin='02',
            loc_tier__loc_tier='A1',
        )

        number_of_boxes = 3
        boxes = self.build_boxes(number_of_boxes)

        product = Product.objects.first()
        exp_year = date.today().year + 3

        pallet = Pallet.objects.create(
            name='gray pallet',
            pallet_status=Pallet.FILL
        )

        # Using PalletBoxes to build form post data
        pallet_boxes = self.build_pallet_boxes(
            pallet,
            boxes,
            product,
            exp_year,
        )
        pallet_boxes[0].exp_month_start = 3
        pallet_boxes[0].exp_month_end = 6

        post_data = self.get_build_pallet_form_post_data(location)
        post_data.update(
            self.get_hidden_pallet_form_post_data(pallet)
        )
        post_data.update(
            self.get_box_forms_post_data(
                pallet_boxes
            )
        )

        user = create_user('alan', 'turing')

        client = Client()
        client.force_login(user)

        response = client.post(
            self.url,
            post_data,
        )

        self.assertEqual(200, response.status_code)

        for i, box in enumerate(boxes):
            box.refresh_from_db()

            self.assertEqual(product, box.product)
            self.assertEqual(location, box.location)
            self.assertEqual(exp_year, box.exp_year)

            if i == 0:
                self.assertEqual(3, box.exp_month_start)
                self.assertEqual(6, box.exp_month_end)

            self.assertEqual(
                1,
                Activity.objects.filter(
                    box_number=box.box_number
                ).count()
            )

        self.assertFalse(Pallet.objects.filter(pk=pallet.pk).exists())
        self.assertFalse(
            PalletBox.objects.filter(
                box_number__in={b.box_number for b in boxes}
            )
        )


class ManualMoveBoxViewTest(TestCase):

    fixtures = (
        'BoxType',
        'ProductCategory',
        'Product',
        'LocRow',
        'LocBin',
        'LocTier',
        'Location',
    )

    url = reverse_lazy('fpiweb:manual_move_box')

    def test_get(self):
        user = User.objects.create_user('jdoe3', 'jdoe2@foo.com', 'abc123')

        client = Client()
        client.force_login(user)

        response = client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
            response.context.get('mode'),
        )

        box_number_form = response.context.get('box_number_form')
        self.assertIsInstance(box_number_form, FilledBoxNumberForm)
        self.assertIsNone(response.context['box'])
        self.assertIsNone(response.context['location_form'])
        self.assertIsNone(response.context['errors'])

    def test_post_box_number_form(self):
        user = User.objects.create_user('jdoe4', 'jdoe4@foo.com', 'abc123')

        client = Client()
        client.force_login(user)

        box_number = BoxNumber.get_next_box_number()

        response = client.post(
            self.url,
            {
                'mode': ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
                'box_number': box_number
            },
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            ManualMoveBoxView.MODE_ENTER_BOX_NUMBER,
            response.context['mode'],
        )
        self.assertIsInstance(
            response.context['box_number_form'],
            FilledBoxNumberForm,
        )

        box = Box.objects.create(
            box_number=box_number,
            box_type=BoxType.objects.get(box_type_code='Evans'),
            product=Product.objects.get(prod_name='Canned Potatoes'),
        )

        # response = client.post(
        #     self.url,
        #     {
        #         'mode': ManualMoveBoxView.MODE_ENTER_BOX_INFO,
        #         'box_number': box_number
        #     }
        # )
        # self.assertEqual(200, response.status_code)
        # self.assertEqual(
        #     ManualMoveBoxView.MODE_ENTER_LOCATION,
        #     response.context['mode'],
        # )
        # self.assertEqual(
        #     response.context['box'].box_number,
        #     box.box_number
        # )
        # self.assertIsInstance(
        #     response.context['location_form'],
        #     ExistingLocationForm,
        # )

    def test_post_location_form(self):
        user = User.objects.create_user('jdoe5', 'jdoe5@foo.com', 'abc123')

        client = Client()
        client.force_login(user)

        box = Box.objects.create(
            box_number=BoxNumber.get_next_box_number(),
            box_type=BoxType.objects.get(box_type_code='Evans'),
            product=Product.objects.get(prod_name='Canned Potatoes'),
            date_filled=timezone.now(),
            exp_year=2022,
            quantity=0,
        )
        self.assertIsNone(box.location)

        location = Location.objects.first()

        response = client.post(
            self.url,
            {
                'mode': ManualMoveBoxView.MODE_ENTER_LOCATION,
                'loc_row': location.loc_row_id,
                'loc_bin': location.loc_bin_id,
                'loc_tier': location.loc_tier_id,
                'box_pk': box.pk,
            }
        )

        self.assertEqual(200, response.status_code, response.content)

        context_box = response.context.get('box')
        self.assertIsNotNone(context_box)
        self.assertEqual(
            box.pk,
            context_box.pk,
        )
        self.assertEqual(
            location.pk,
            context_box.location.pk,
        )


class TestBoxItemFormView(TestCase):

    def test_get_form(self):
        box_number = BoxNumber.format_box_number(15)
        pallet_box = PalletBox(
            box_number=box_number,
        )
        form = BoxItemFormView.get_form(pallet_box)
        self.assertIsNotNone(form)
        self.assertIsNone(form.prefix)
        self.assertEqual(
            box_number,
            form.initial['box_number']
        )


class ManualPalletMoveViewTest(TestCase):

    fixtures = (
        'BoxType',
        'Constraints',
        'Location',
        'LocBin',
        'LocRow',
        'LocTier',
        'Product',
        'ProductCategory',
    )

    url = reverse_lazy('fpiweb:manual_pallet_move')

    def test_get(self):

        client = logged_in_user('fred', 'roush')

        response = client.get(self.url)
        self.assertEqual(200, response.status_code)

        context = response.context
        self.assertEqual(
            ManualPalletMoveView.MODE_ENTER_FROM_LOCATION,
            context['mode']
        )
        self.assertIsInstance(
            context.get('from_location_form'),
            ExistingLocationWithBoxesForm,
        )

    def test_post__missing_mode(self):

        client = logged_in_user('emily', 'franzese')

        response = client.post(self.url)
        self.assertContains(response, "Missing mode parameter", status_code=400)

        context = response.context
        self.assertEqual(
            ManualPalletMoveView.MODE_ENTER_FROM_LOCATION,
            context['mode']
        )
        self.assertIsInstance(
            context.get('from_location_form'),
            ExistingLocationWithBoxesForm,
        )

    def test_post__unrecognized_mode(self):

        client = logged_in_user('kaitlin', 'kostiv')

        mode = 'A suffusion of yellow'
        response = client.post(self.url, {'mode': mode})
        self.assertContains(
            response,
            f"Unrecognized mode {mode} in ManualPalletMoveView",
            status_code=400,
        )

    def test_post_from_location_form__form_invalid(self):

        client = logged_in_user('Jerlene', 'Elder')

        mode = ManualPalletMoveView.MODE_ENTER_FROM_LOCATION

        response = client.post(self.url, {'mode': mode})
        self.assertContains(
            response,
            'This field is required.',
            status_code=400,
        )

        context = response.context
        self.assertEqual(
            mode,
            context['mode'],
        )
        self.assertIsInstance(
            context['from_location_form'],
            ExistingLocationWithBoxesForm,
        )

    def test_post_from_location_form__form_valid(self):
        client = logged_in_user('Jerlene', 'Elder')

        mode = ManualPalletMoveView.MODE_ENTER_FROM_LOCATION

        location = Location.get_location('01', '01', 'B1')

        Box.objects.create(
            box_type=Box.box_type_default(),
            box_number=BoxNumber.format_box_number(42),
            location=location,
        )

        response = client.post(
            self.url,
            {
                'mode': mode,
                'from-loc_row': location.loc_row.pk,
                'from-loc_bin': location.loc_bin.pk,
                'from-loc_tier': location.loc_tier.pk,
            }
        )
        self.assertEqual(
            200,
            response.status_code,
            response.content.decode()
        )
        self.assertEqual(
            ManualPalletMoveView.MODE_ENTER_TO_LOCATION,
            response.context.get('mode'),
        )
        form = response.context.get('to_location_form')
        self.assertIsInstance(form, MoveToLocationForm)

    def test_post_to_location_form__form_invalid(self):
        client = logged_in_user('Jerlene', 'Elder')

        mode = ManualPalletMoveView.MODE_ENTER_TO_LOCATION

        response = client.post(self.url, {'mode': mode})
        self.assertContains(
            response,
            "This field is required.",
            status_code=400,
        )

        context = response.context
        self.assertEqual(mode, context['mode'])
        self.assertIsInstance(
            context['to_location_form'],
            MoveToLocationForm,
        )

    @staticmethod
    def build_to_location_form_post_data(from_location, to_location):
        mode = ManualPalletMoveView.MODE_ENTER_TO_LOCATION
        prefix = ManualPalletMoveView.FORM_PREFIX_TO_LOCATION
        return {
            'mode': mode,
            f'{prefix}-from_location': from_location.pk,
            f'{prefix}-loc_row': to_location.loc_row.pk,
            f'{prefix}-loc_bin': to_location.loc_bin.pk,
            f'{prefix}-loc_tier': to_location.loc_tier.pk,
        }

    def test_post_to_location_form__boxes_in_to_location(self):
        client = logged_in_user('Jerlene', 'Elder')

        from_location = Location.get_location('01', '01', 'B1')
        to_location = Location.get_location('02', '02', 'B1')

        Box.objects.create(
            box_type=Box.box_type_default(),
            location=to_location,
        )

        response = client.post(
            self.url,
            self.build_to_location_form_post_data(from_location, to_location)
        )
        self.assertEqual(200, response.status_code, response.content.decode())
        self.assertEqual(
            ManualPalletMoveView.MODE_CONFIRM_MERGE,
            response.context['mode'],
        )
        self.assertIsInstance(
            response.context['confirm_merge_form'],
            ConfirmMergeForm,
        )

    def test_post_to_location_form__move_complete(self):
        client = logged_in_user('Jerlene', 'Elder')

        from_location = Location.get_location('01', '03', 'A1')
        to_location = Location.get_location('01', '03', 'A2')

        box = Box.objects.create(
            box_type=Box.box_type_default(),
            location=from_location,
            product=Product.objects.first(),
            exp_year=timezone.now().year + 2,
        )

        response = client.post(
            self.url,
            self.build_to_location_form_post_data(from_location, to_location)
        )
        self.assertEqual(200, response.status_code, response.content.decode())
        self.assertEqual(
            ManualPalletMoveView.MODE_COMPLETE,
            response.context['mode'],
        )
        box.refresh_from_db()
        self.assertEqual(
            to_location.id,
            box.location_id,
        )
        self.assertContains(
            response,
            '1 boxes moved to: row 01, bin 03, tier A2.'
        )

    def test_post_confirm_merge_form__form_invalid(self):
        client = logged_in_user('Jeremy', 'Bearimy')

        mode = ManualPalletMoveView.MODE_CONFIRM_MERGE

        response = client.post(
            self.url,
            {
                'mode': mode,
            }
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(mode, response.context['mode'])
        self.assertIsInstance(
            response.context['confirm_merge_form'],
            ConfirmMergeForm,
        )

    @staticmethod
    def build_confirm_merge_post_data(from_location, to_location, action):
        prefix = ManualPalletMoveView.FORM_PREFIX_CONFIRM_MERGE
        return {
            f'mode': ManualPalletMoveView.MODE_CONFIRM_MERGE,
            f'{prefix}-from_location': from_location.pk,
            f'{prefix}-to_location': to_location.pk,
            f'{prefix}-action': action,
        }

    def test_post_confirm_merge_form__action_change_location(self):
        client = logged_in_user('Jeremy', 'Bearimy')

        from_location = Location.get_location('02', '02', 'A1')
        to_location = Location.get_location('02', '02', 'C1')

        response = client.post(
            self.url,
            self.build_confirm_merge_post_data(
                from_location,
                to_location,
                ConfirmMergeForm.ACTION_CHANGE_LOCATION,
            )
        )

        self.assertEqual(200, response.status_code, response.content.decode())
        self.assertEqual(
            ManualPalletMoveView.MODE_ENTER_TO_LOCATION,
            response.context['mode'],
        )
        self.assertIsInstance(
            response.context['to_location_form'],
            MoveToLocationForm
        )

    def test_post_confirm_merge_form__action_merge_pallets(self):
        client = logged_in_user('Jeremy', 'Bearimy')

        from_location = Location.get_location('02', '02', 'A1')
        to_location = Location.get_location('02', '02', 'C1')

        box = Box.objects.create(
            box_type=Box.box_type_default(),
            location=from_location,
            product=Product.objects.first(),
            exp_year=timezone.now().year + 2
        )

        response = client.post(
            self.url,
            self.build_confirm_merge_post_data(
                from_location,
                to_location,
                ConfirmMergeForm.ACTION_MERGE_PALLETS,
            )
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ManualPalletMoveView.MODE_COMPLETE,
            response.context['mode'],
        )
        box.refresh_from_db()
        self.assertEqual(
            to_location.id,
            box.location_id,
        )
        self.assertContains(response, '1 boxes moved to: row 02, bin 02, tier C1.')

